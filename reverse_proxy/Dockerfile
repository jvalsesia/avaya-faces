FROM nginx:1.21-alpine

COPY cert.pem /etc/ssl/certs/nginx/
COPY key.pem /etc/ssl/certs/nginx/

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d

EXPOSE 8080
EXPOSE 443