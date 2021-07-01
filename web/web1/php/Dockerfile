FROM php:7.2.7-fpm-alpine3.7
RUN apk update; \
    apk upgrade;

RUN apk update && \
    apk add --no-cache git perl && \
    cd /tmp && \
    git clone https://github.com/jasonm23/cowsay.git  && \
    cd cowsay ; ./install.sh /usr/local && \
    rm -rf /var/cache/apk/* /var/tmp/* /tmp/* && \
    apk del git

COPY flag.txt /flag.txt
RUN chown root:root /flag.txt
RUN chmod 755 /flag.txt

RUN docker-php-ext-install mysqli
