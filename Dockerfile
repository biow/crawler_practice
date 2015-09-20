FROM ubuntu:14.04

ENV DEBIAN_FRONTEND noninteractive

# Repos
RUN apt-get -y update

# Install
RUN apt-get install -y git vim python-pip python2.7-dev wget curl python-matplotlib

# Install python packages
RUN pip install nose ipython[notebook]

# Configure bash and vim
WORKDIR /root
ADD home_file/ /root/

# Default
WORKDIR /share
