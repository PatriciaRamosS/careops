from pathlib import Path
from typing import Optional

from fastapi import FastAPI, Request, Query, HTTPException
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.templating import Jinja2Templates

# Caminho base para achar a pasta de templates
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

app = FastAPI(
    title="CareOps+ API",
    version="0.1.0",
    description="Mini aplicação de exemplo para a disciplina de Segurança de Aplicações (DevSecOps)."
)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """
    Página inicial HTML da aplicação (equivalente ao render_template do Flask).
    Mostra um formulário simples que usa o endpoint /sum.
    """
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "CareOps+ - Calculadora simples",
        },
    )


@app.get("/health")
async def health():
    """
    Healthcheck simples.
    Usado em CI/CD e monitoramento.
    """
    return {"status": "ok"}


@app.get("/sum")
async def sum_route(
    a: Optional[float] = Query(None, description="Primeiro valor da soma"),
    b: Optional[float] = Query(None, description="Segundo valor da soma"),
):
    """
    Endpoint de soma simples (equivalente ao /sum do Flask).
    Exemplo: GET /sum?a=2&b=3  ->  {"result": 5}
    """
    if a is None or b is None:
        # Erro semelhante ao do Flask quando parâmetros estão ausentes/invalidos
        raise HTTPException(status_code=400, detail="missing parameters 'a' and/or 'b'")

    try:
        result = float(a) + float(b)
    except (TypeError, ValueError):
        raise HTTPException(status_code=400, detail="invalid parameters")

    return {"result": result}


# Opcional: endpoint JSON só para debug/uso em aula
@app.get("/info")
async def info():
    """
    Endpoint JSON com informações básicas da API.
    Útil para demonstrações e testes automatizados.
    """
    return {
        "app": "CareOps+ API",
        "version": "0.1.0",
        "endpoints": ["/", "/health", "/sum", "/info"],
    }