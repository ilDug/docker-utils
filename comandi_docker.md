# Docker - Comandi Utili

## Eseguire un comando in un container attivo

```bash
docker exec -it <container_name> <command>
```


## Eseguire un comando in un NUOVO container

e poi li rimuove subito

```bash
docker run -it -rm <image> <command>
```

## Crea un immagine

```bash
#salva in local
docker build --progress=tty -t <image_name:version> -f <./Dockerfile.prod> <path>

# salva direttamente in un file
docker build --progress=tty -t <image_name:version> -f <./Dockerfile.prod> -o - > image_name.version.tar <path>

# esempio 
docker build --progress=tty -t dagtest:1.0.5 -f Dockerfile -o - > dagtest.1.0.5.tar ./
```



## salva un immagine o la carica
```bash
# salva e carica direttamente
docker save <image> | gzip | pv | ssh user@host docker load
docker save <image> | gzip | pv | DOCKER_HOST=ssh://user@remotehost docker load

docker save dagtest:1.0.1  > dagtest.1.0.1.tar


```

