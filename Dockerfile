# syntax=docker/dockerfile:1

# using latest ubuntu image
FROM python:3.8-slim-buster

# meta-data
LABEL maintainer="edm18b037@iiitdm.ac.in"
LABEL version="1.0"

# setting working directory
WORKDIR /nibble-sim/nibble-sim

# copy all the content from current directory
COPY . ../

# install the required packages
RUN pip3 install -r ../requirements.txt

ENTRYPOINT ["python3", "/nibble-sim/nibble-sim/nibble_sim.py"]