FROM python:3.13-slim-bullseye

WORKDIR /app

COPY requirements.txt requirements.txt
COPY hello.py hello.py
RUN pip3 install -r requirements.txt
#ENV FLASK_APP=hello

ENTRYPOINT [ "python", "-u", "-m", "flask", "--app", "hello", "run", "--host", "0.0.0.0"]
