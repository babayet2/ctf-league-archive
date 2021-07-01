FROM python:3

# @AUTHOR: build requirements here
RUN useradd chal

WORKDIR /chal

# @AUTHOR: make sure all source is copied in. If everything is in src/, no change needed
COPY src/ ./
RUN pip install -r requirements.txt

ENV FLASK_APP=server.py

RUN chown -R root:root /chal/*
RUN chmod -R o-w /chal/*

COPY flag /flag
RUN chown -R root:root /flag
RUN chmod -R o-w /flag

# run challenge
EXPOSE 5000

CMD ["gunicorn", "-w=2", "-b 0.0.0.0:5000", "server:app"]
