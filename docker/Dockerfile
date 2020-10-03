
FROM debian:buster-slim

LABEL maintainer="esteban@gominet.net"
LABEL version="0.1.0"

# En entornos windows, se atasca un poco con proxy, virtualizacion de red, etc.. , hay que 
# dejarle aire para establecer las conexiones.
#
ARG PIP_DEFAULT_TIMEOUT=100
ENV PIP_DEFAULT_TIMEOUT=${PIP_DEFAULT_TIMEOUT}

# En desarrollo, para reducir las operaciones.
RUN apt-get update 
RUN apt-get install -y \
	less \
	nano \
	rsync \
	unzip \
	vim-tiny \
	zip
RUN apt-get install -y \
	python3 \
	python3-pip \
	&& rm -rf /var/lib/apt/lists/*
RUN pip3 install virtualenv \
	tox \
	pylama \
	bandit \
	&& mkdir -p /pythondev/output /pythondev/tests /mnt/git
WORKDIR /mnt/git

ADD docker/rsyncdev.sh /pythondev/rsyncdev.sh
