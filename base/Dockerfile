# we'll use the base ubuntu:focal image
FROM ubuntu:focal

# install julia and python3 for our demo
RUN apt-get update && apt install -y julia python3

# required to avoid tzdata prompt
RUN ln -fs /usr/share/zoneinfo/America/Los_Angeles /etc/localtime

# install python dependencies
RUN apt install -y python3-numpy python3-matplotlib python3-keras

# install flask
RUN apt install -y python3-flask

# install h5py
RUN apt install -y python3-h5py

# install curl
RUN apt install -y curl

# create a non-root user
RUN useradd -m demouser

# switch as the user
USER demouser

# This is the base directory
WORKDIR /home/demouser
