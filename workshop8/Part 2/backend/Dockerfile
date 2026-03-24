FROM python:3.13-trixie
# FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
COPY data/*csv data/
COPY datacompass.py .
COPY utils.py .

RUN apt -y update 
RUN apt -y upgrade
RUN apt -y install graphviz graphviz-dev
# RUN apt-get update && apt-get install -y --no-install-recommends \
#     gcc \
#     graphviz \
#     libgraphviz-dev \
#     pkg-config \
#     python3-dev \
#     && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

ENTRYPOINT [ "python", "-u", "-m", "flask", "-A", "datacompass", "run", "--reload", "--port=5000", "--host=0.0.0.0"]

# -u: force unbuffered output (useful in Docker logs)

# --reload: enable auto-reloading on code changes (dev only)

# "--host=0.0.0.0": make it accessible externally

# "--port=5000": set port Flask listens on (5000 by default)
#                not compulsory, wile good to have for readability. 