# IMAGE 1: build challenge
# @AUTHOR: if your chal doesn't build seperately from being run (i.e. Python),
#          delete all of the IMAGE 1 code

#WORKDIR /build

# @AUTHOR: make sure all source is copied in. If everything is in src/, no change needed
#COPY src ./src/
#COPY Makefile .
#RUN make container

# IMAGE 2: run challenge
# @AUTHOR: feel free to change base image as necessary (i.e. python, node)
FROM python:3.8

RUN pip3 install numpy

# copy trustee
WORKDIR /chal
# @AUTHOR: make sure all build outputs are copied to the runner
#          if there is no build output, replace this with the appropriate COPY stmts
#          to pull files from the host
COPY lyells_bot.py ./lyells_bot.py
COPY common.py ./common.py

RUN mkdir -p data

# copy public_key
COPY  data/public_key /chal/data

# make user
RUN useradd chal

# Set perms
RUN chown -R root:root /chal/*
RUN chmod -R o-w /chal/*

# run challenge
EXPOSE 23450
CMD ["python3", "lyells_bot.py"]
