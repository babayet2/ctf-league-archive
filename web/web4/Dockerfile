# Set the base image
FROM debian:latest

RUN apt-get update && apt-get install -y apache2 \
    libapache2-mod-wsgi \
    build-essential \
    python \
    python-dev\
    python-pip \
    vim \
    openssh-client \
    openssh-server \ 
    supervisor \
 && apt-get clean \
 && apt-get autoremove \
 && rm -rf /var/lib/apt/lists/*

# Copy over and install the requirements
COPY ./app/requirements.txt /var/www/apache-flask/app/requirements.txt
RUN pip install -r /var/www/apache-flask/app/requirements.txt

# Setup supervisord
RUN mkdir -p /var/lock/apache2 /var/run/apache2 /var/run/sshd /var/log/supervisor
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Copy over the apache configuration file and enable the site
COPY ./apache-flask.conf /etc/apache2/sites-available/apache-flask.conf
RUN a2ensite apache-flask && \
    a2enmod headers

# Copy over the wsgi file
COPY ./apache-flask.wsgi /var/www/apache-flask/apache-flask.wsgi

# Create wsgi user + create debug key
RUN useradd -m fwsgi \
  && su fwsgi -c 'yes "" | ssh-keygen -q -N ""'

# Copy over some files we're gonna provide source of
COPY ./apache-flask.conf /var/www/apache-flask/app/static/apache-flask.conf
COPY ./Dockerfile /var/www/apache-flask/app/static/Dockerfile
COPY ./docker-compose.yml /var/www/apache-flask/app/static/docker-compose.yml
COPY ./app/routes.py /var/www/apache-flask/app/static/routes.py

COPY ./flag.txt /flag.txt
COPY ./run.py /var/www/apache-flask/run.py
COPY ./app /var/www/apache-flask/app/

RUN a2dissite 000-default.conf && \
    a2ensite apache-flask.conf && \
    echo 'ulimit -v 148576' >> /etc/default/apache2 && \
    service ssh start

# LINK apache config to docker logs.
RUN ln -sf /proc/self/fd/1 /var/log/apache2/access.log && \
    ln -sf /proc/self/fd/1 /var/log/apache2/error.log && \
    chmod 444 /flag.txt && \
    chown root:root /flag.txt

EXPOSE 8180
EXPOSE 22

WORKDIR /var/www/apache-flask

CMD ["/usr/bin/supervisord"]
