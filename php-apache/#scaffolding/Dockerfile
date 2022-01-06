FROM php:8-apache

RUN apt-get update && \
    apt-get install -y  \ 
    ca-certificates  \
    software-properties-common  \
    nano \
    gnupg  \ 
    zip \
    wget   \
    curl \
    && apt-get clean -y

# abilitazione de moduli  di APACHE e della configurazione del sito
RUN a2enmod rewrite && \
    a2enmod headers && \
    service apache2 restart
# a2enmod ssl && \
# a2dissite 000-default && \
# a2ensite site-ssl.conf && \
# a2ensite site-http.conf && \

# RUN apt-get install -y  \ 
#     libxml2-dev \
#     libzip-dev \
#     libsodium-dev \
#     libcurl4-gnutls-dev

# RUN docker-php-ext-install pdo pdo_mysql mysqli zip sodium xml curl
# RUN docker-php-ext-enable pdo pdo_mysql mysqli zip sodium xml curl

# RUN docker-php-ext-install  mbstring imap
# RUN docker-php-ext-enable  mbstring imap

# porta
EXPOSE 80

# RUN mkdir -p /run/systemd && echo 'docker' > /run/systemd/container
# CMD service apache2 start & tail -f /var/log/apache2/*
# CMD ["apache2-foreground"]


# !!!!!!!!!! MODIFICARE AD OGNI CAMBIAMENTO
# docker build  -t ildug/php-apache:8.0-web .
# docker push ildug/php-apache:8.0-web
# docker run -d --name test_1  -p 8080:80 -v ./:/var/www/html/  ildug/php-apache:8.0-web
# docker exec -it test_1 bash
