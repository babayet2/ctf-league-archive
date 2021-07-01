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

ARG TrusteeId=0
ENV trustee_id $TrusteeId

ARG TrusteePort=31306
ENV trustee_port $TrusteePort

# copy trustee
WORKDIR /chal
# @AUTHOR: make sure all build outputs are copied to the runner
#          if there is no build output, replace this with the appropriate COPY stmts
#          to pull files from the host
COPY trustee.py ./trustee.py
COPY common.py ./common.py
COPY zkp.py ./zkp.py

RUN mkdir -p /chal/data

# copy flag shares
COPY  data/flag${TrusteeId} /chal/data

# copy private_key
COPY  data/private_key${TrusteeId} /chal/data

# copy public_key
COPY  data/public_key /chal/data

# make user
RUN useradd chal

# Set perms
RUN chown -R root:root /chal/*
RUN chmod -R o-w /chal/*

# run challenge
EXPOSE $TrusteePort
ENTRYPOINT python3 trustee.py ${trustee_id}
