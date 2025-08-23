from fastapi.openapi.utils import get_openapi
from backend.main import app
import json

spec = get_openapi(
  title=app.title,
  version=app.version,
  openapi_version=app.openapi_version,
  description=app.description,
  routes=app.routes,
)
# Remove 422 responses and their related schemas because the Dart client generator cannot handle ValidationError properly
# for path in spec["paths"]:
#   for verb in spec["paths"][path]:
#     spec["paths"][path][verb]["responses"] = {k: v for k, v in spec["paths"][path][verb]["responses"].items() if k not in ["422"]}
# spec["components"]["schemas"] = {k: v for k, v in spec["components"]["schemas"].items() if k not in ["HTTPValidationError", "ValidationError"]}

spec["paths"] = {k: v for k, v in spec["paths"].items() if k not in ["/docs", "/openapi.json"]}
# del spec["paths"]["/test_outbound_email"]

with open('api/spec.json', 'w') as f:
  json.dump(spec, f, indent=2)
