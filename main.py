import logging
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.templating import Jinja2Templates

# Configuração de logging (de propósito um pouco "inseguro")
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("careops")

app = FastAPI(
    title="CareOps+ API (Aula 2 – Versão Vulnerável)",
    version="0.2.0",
    description="Versão da aplicação com vulnerabilidades intencionais para estudo OWASP."
)

templates = Jinja2Templates(directory="templates")

# -------------------------------------------------------
# Página inicial – usa o index.html que você enviou
# -------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "title": "CareOps+ · DevSecOps Lab"
        }
    )


# -------------------------------------------------------
# Healthcheck básico (usado pela UI e pelo CI/CD)
# -------------------------------------------------------
@app.get("/health")
async def health():
    return {"status": "ok"}


# -------------------------------------------------------
# /sum – usado pela calculadora da UI
# - Com validação fraca (para discutirmos riscos)
# -------------------------------------------------------
@app.get("/sum")
async def sum_route(a: str = "0", b: str = "0"):
    try:
        x = float(a)
        y = float(b)
    except ValueError:
        # Loga parâmetros como texto (pode vazar entrada maliciosa)
        logger.warning(f"[SUM] Parâmetros inválidos recebidos: a={a}, b={b}")
        return JSONResponse({"detail": "parâmetros inválidos"}, status_code=400)

    result = x + y
    logger.info(f"[SUM] a={a}, b={b}, result={result}")
    return {"result": result}


# -------------------------------------------------------
# /echo – reflete entrada sem sanitização (XSS / Injection)
# Não aparece na UI, mas é ótimo para análise OWASP.
# -------------------------------------------------------
@app.get("/echo", response_class=HTMLResponse)
async def echo(msg: str = ""):
    # Vulnerabilidade: reflete o input diretamente em HTML
    html = f"""
    <html>
      <head><title>Echo</title></head>
      <body>
        <h1>Echo</h1>
        <p>{msg}</p>
        <p><a href="/">Voltar</a></p>
      </body>
    </html>
    """
    logger.info(f"[ECHO] msg={msg}")
    return HTMLResponse(content=html)


# -------------------------------------------------------
# /patient/{id} – Broken Access Control + exposição de dados
# (sem autenticação/autorização)
# -------------------------------------------------------
fake_db = {
    "1": {"id": 1, "name": "João Silva", "diagnosis": "Hipertensão"},
    "2": {"id": 2, "name": "Maria Oliveira", "diagnosis": "Asma"},
}

@app.get("/patient/{patient_id}")
async def get_patient(patient_id: str):
    logger.info(f"[INSECURE LOG] Consulta ao paciente {patient_id}")
    if patient_id in fake_db:
        return fake_db[patient_id]
    return JSONResponse({"error": "not found"}, status_code=404)


# -------------------------------------------------------
# /debug/config – exposição de segredos (A02, A09)
# -------------------------------------------------------
@app.get("/debug/config")
async def debug_config():
    # Esses valores são intencionalmente inseguros para estudo
    config = {
        "SECRET_KEY": "123456",
        "DB_PASSWORD": "senha_super_secreta",
        "DEBUG_MODE": True
    }
    logger.warning(f"[CRITICAL] Configuração sensível exposta: {config}")
    return config
