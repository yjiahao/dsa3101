FROM quay.io/jupyter/base-notebook
RUN pip install --no-cache-dir pandas folium pyproj

WORKDIR /home/week3/work
COPY hdb_carparks.ipynb .
COPY HDBCarparkInformation.csv .

# docker build -t test-01 ./
# docker run --rm -p 8899:8888 test-01:latest start-notebook.py --NotebookApp.token='my-token'
