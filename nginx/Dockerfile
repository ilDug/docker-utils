FROM nginx:latest

COPY ./conf /etc/nginx/conf.d
COPY ./apps /usr/share/nginx/html


# docker build --progress=tty -t multiweb:1.0.5 -f Dockerfile -o - > multiweb.1.0.5.tar ./
# docker build --progress=tty -t multiweb:1.0.5  ./

# docker save multiweb:1.0.5 | gzip | pv | ssh root@docker1.eurokemical.lan docker load