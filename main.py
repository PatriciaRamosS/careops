from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates
from pydantic import ValidationError
from typing import Dict

from database import load_db, save_db


app = FastAPI(title="CareOps+ API", version="0.2.0")

templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def root(request: Request):
    return templates.TemplateResponse(
        "index.html", {"request": request, "title": "CareOps+ Aula 2"}
    )


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/sum")
def sum_route(a: str, b: str):
    # Vulnerável: validação fraca
    try:
        result = float(a) + float(b)
    except Exception as e:
        print(f"[DEBUG] erro somando: {e} com valores a={a}, b={b}")
        return JSONResponse(
            {"error": "invalid parameters"}, status_code=400
        )
    return {"result": result}


@app.get("/echo")
def echo(msg: str):
    # Vulnerável: refletindo entrada no HTML
    return HTMLResponse(f"<h3>Eco:</h3><p>{msg}</p>")


@app.get("/patients")
def get_patients():
    db = load_db()
    # Vulnerável: sem autenticação, exibe tudo
    return db["patients"]


@app.get("/patient/{id}")
def get_patient(id: int):
    db = load_db()
    patient = db["patients"].get(str(id))
    if not patient:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")
    return patient


@app.post("/patients")
def create_patient(payload: Dict):
    """
    Vulnerabilidades:
    - sem validação de tipos (A03)
    - campos permitidos não controlados (A04, insecure design)
    - log inseguro
    """
    print(f"[DEBUG] Criando paciente com payload inseguro: {payload}")

    db = load_db()
    new_id = max(map(int, db["patients"].keys())) + 1
    payload["id"] = new_id

    db["patients"][str(new_id)] = payload
    save_db(db)
    return {"message": "Paciente criado", "patient": payload}


@app.delete("/patients/{id}")
def delete_patient(id: int):
    db = load_db()

    # Vulnerável: qualquer um pode apagar
    deleted = db["patients"].pop(str(id), None)
    save_db(db)

    if not deleted:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    return {"message": "Paciente removido", "patient": deleted}


@app.put("/patients/{id}")
def update_patient(id: int, payload: Dict):
    db = load_db()

    # Vulnerável: sobrescreve tudo sem checar estrutura
    if str(id) not in db["patients"]:
        raise HTTPException(status_code=404, detail="Paciente não encontrado")

    print(f"[DEBUG] Atualizando paciente: {payload}")

    payload["id"] = id
    db["patients"][str(id)] = payload
    save_db(db)

    return {"message": "Paciente atualizado", "patient": payload}


@app.get("/debug/config")
def debug_config():
    # EXPOSTO DE PROPÓSITO (para aula OWASP)
    return {
        "debug": True,
        "secret_key": "123456",
        "database_path": "patients.json",
        "environment": "development"
    }
