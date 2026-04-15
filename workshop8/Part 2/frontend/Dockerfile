FROM python:3.10-slim
WORKDIR /app/frontend
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY data/*csv data/
COPY . .
CMD ["streamlit", "run", "frontend.py", "--server.port=8501", "--server.address=0.0.0.0"]

# Use "--server.address=0.0.0.0" to make it accessible outside the container.

# "--server.port=8501" specifies the port in the container (8501 by default).
# "--server.port=8501" is optional unless you want to use a different port, 
# while it is good to have for readability. 
