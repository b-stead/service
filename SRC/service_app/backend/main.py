from fastapi import FastAPI, HTTPException, status
from backend.db import Healthcheck
from fastapi.openapi.docs import get_swagger_ui_html

from .routers import user
from .routers import customers
from .routers import auth

app = FastAPI(
    title="Service App",
)

app.include_router(user.router)
app.include_router(customers.router)
app.include_router(auth.router)


@app.get("/docs")
async def custom_docs():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/healthz", response_model=str)
def healthz(healthcheck: Healthcheck) -> str:
  if not healthcheck:
    raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE)
  return "ok"