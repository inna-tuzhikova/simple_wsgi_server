FROM python:3.7-slim
WORKDIR /app

COPY server.py /app/
CMD ["python", "/app/server.py"]
