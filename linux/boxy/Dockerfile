FROM debian:latest

#Install and configure necessary tools
RUN apt update 
RUN apt -y upgrade 
RUN apt install -y openssh-server python3-pip netcat net-tools sudo --fix-missing
RUN mkdir /var/run/sshd
COPY ssh/sshd_config /etc/ssh/sshd_config
RUN chmod 644 /etc/ssh/sshd_config
EXPOSE 13337 1337 1338

#Change root password

RUN useradd -m -d /home/fred -s /bin/bash frederick
RUN mkdir /home/fred/.ssh
COPY listener/key.priv.pub /home/fred/.ssh/authorized_keys
RUN chmod 700 /home/fred/.ssh
RUN chmod 600 /home/fred/.ssh/authorized_keys
RUN chown -R frederick:frederick /home/fred/.ssh

COPY sudo/sudoers /etc/sudoers
RUN chmod 644 /etc/sudoers
RUN mkdir -p /root/script/
COPY skel/add_dog.sh /root/script/adopt_dog
RUN chmod 555 /root/
RUN chmod 555 /root/script/
RUN chmod 544 /root/script/adopt_dog

COPY ssh/.ssh /root/.ssh
RUN chmod 700 /root/.ssh
RUN chmod 600 /root/.ssh/*

COPY bash/.bashrc /root/.bashrc
RUN chmod 600 /root/.bashrc

COPY shadow/shadow.bak /etc/shadow.bak
RUN chmod 644 /etc/shadow.bak

RUN useradd -m -d /home/admin -s /bin/bash oldadmin
RUN echo "oldadmin:freedom42" | chpasswd
COPY shadow/top_100_password_ideas /home/fred/
COPY shadow/password_guide /home/fred/

COPY /opt/what /opt/what
RUN chmod -R 700 /opt/what

COPY skel/skel_flag /etc/skel/flag
RUN chmod 600 /etc/skel/flag
#Set up user directory
#RUN echo cd /app/crow/shamir/code >> /root/.bashrc

#Change setting file to reflect node ID
#ARG ID
#RUN sed -i "s/'auth'/'$ID'/" /app/crow/shamir/code/settings.py

RUN mkdir /root/listeners 
RUN chmod 700 /root/listeners
COPY listener/key.priv /root/listeners/
COPY listener/listener.py /root/listeners/
COPY localhost/listener.py /root/listeners/localhost.py

#Start ssh servers
COPY runme /opt/runme
RUN chmod 700 /opt/runme


CMD ["/opt/runme"]
