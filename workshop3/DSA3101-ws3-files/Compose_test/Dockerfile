FROM python:3.13-slim-bullseye
WORKDIR /code

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY app.py app.py

ENTRYPOINT [ "python", "-u", "-m", "flask", "run", "--host", "0.0.0.0"]
