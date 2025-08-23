FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt && mkdir backend
EXPOSE 8000
COPY . backend
CMD ["uvicorn", "backend.main:app", "--log-config=backend/uvicorn_log_config.yaml", "--host=0.0.0.0", "--port=8000"]