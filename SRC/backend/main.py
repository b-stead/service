from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html

app = FastAPI(
    title="Service App",
)


@app.get("/docs")
async def custom_docs():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}