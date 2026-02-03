FROM python:3.13-slim-bullseye
WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY uv_index_request.py uv_index_request.py

CMD ["python", "uv_index_request.py"]