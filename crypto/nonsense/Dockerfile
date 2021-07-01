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
FROM ubuntu:18.04

# @AUTHOR: run requirements here
RUN apt-get -qq update && apt-get -qq --no-install-recommends install xinetd python3 python3-pip
RUN pip3 install pycryptodome

# copy binary
WORKDIR /chal
# @AUTHOR: make sure all build outputs are copied to the runner
#          if there is no build output, replace this with the appropriate COPY stmts
#          to pull files from the host
COPY nonsense.py /chal/chal.py

# copy flag
COPY flag /chal/

# make user
RUN useradd chal

# copy service info
COPY container_src/* /

# Set perms
RUN chown -R root:root /chal/*
RUN chmod -R o-w /chal/*

# run challenge
EXPOSE 31306
RUN chmod +x /run_chal.sh
CMD ["/usr/sbin/xinetd", "-syslog", "local0", "-dontfork", "-f", "/xinetd.conf"]
