## Generators
### sqlc

Firstly, [sqlc](https://sqlc.dev/) takes the database schema and queries in [`repository`](../repository/) and generates a Python database client and [Pydantic](https://docs.pydantic.dev/latest/) models in [`backend/repository`](../backend/repository/). 

Running ['gen.sh'] will create the files

### FastAPI

The `backend` service is based on [FastAPI](https://fastapi.tiangolo.com/). We can use the database client produced by sqlc to query the database using type-safe methods. The data models are automatically used by FastAPI to validate data in API requests and responses.

FastAPI can also generate an OpenAPI specification to match our implementation. This means we end up with an OpenAPI specification that reflects both the data model defined in the database and the API implementation we write in `backend`. The helper script [`backend/gen.py`](../backend/gen.py) uses FastAPI to generate [`api/spec.json`](../api/spec.json).

