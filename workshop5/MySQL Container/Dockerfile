# Use official MySQL image as base
FROM mysql:8.0-debian

# Set environment variables for MySQL root password and default database
#ENV MYSQL_ROOT_PASSWORD=dsa3101
#ENV MYSQL_DATABASE=sakila

COPY my.cnf /etc/mysql/my.cnf

# Download the sakila schema and data from MySQL
RUN apt update 
RUN apt install -y wget unzip 
RUN wget https://downloads.mysql.com/docs/sakila-db.tar.gz 
RUN mkdir /sakila 
RUN cd /sakila
RUN tar -xvzf sakila-db.tar.gz 
RUN cat sakila-db/sakila-schema.sql sakila-db/sakila-data.sql > /docker-entrypoint-initdb.d/01-sakila.sql
COPY sakila2.sql /docker-entrypoint-initdb.d/02-sakila.sql
# RUN rm sakila-db.tar.gz

# Expose MySQL port
EXPOSE 3306
