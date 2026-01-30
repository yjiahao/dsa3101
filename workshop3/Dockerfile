FROM nginx:latest

RUN apt update
RUN apt upgrade -y
RUN apt install -y vim

COPY song2.html /usr/share/nginx/html/
