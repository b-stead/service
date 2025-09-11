from fastapi import FastAPI, HTTPException, status
from backend.db import Healthcheck
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import HTMLResponse
from .routers import user
from .routers import customers
from .routers import auth

app = FastAPI(
    title="Service App",
)

corsOrigins = [
  "http://localhost",
  "http://localhost:8000",
  "http://localhost:8080",
  "http://localhost:3000",
  "http://127.0.0.1:3000",
]
app.add_middleware(CORSMiddleware, allow_origins=corsOrigins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

app.include_router(user.router)
app.include_router(customers.router)
app.include_router(auth.router)


@app.get("/docs", response_class=HTMLResponse)
async def custom_docs() -> HTMLResponse:
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.get("/healthz", response_model=str)
def healthz(healthcheck: Healthcheck) -> str:
    if not healthcheck:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
    return "ok"
