FROM httpd:2.4.33-alpine
RUN apk update; \
    apk upgrade;

# Copy apache vhost file to proxy php requests to php-fpm container
COPY demo.apache.conf /usr/local/apache2/conf/demo.apache.conf
COPY flag.txt /flag.txt

RUN chown root:www-data /flag.txt /usr/local/apache2/conf/demo.apache.conf
RUN chmod 755 /flag.txt /usr/local/apache2/conf/demo.apache.conf

RUN echo "Include /usr/local/apache2/conf/demo.apache.conf" \
    >> /usr/local/apache2/conf/httpd.conf
    
