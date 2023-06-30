FROM python:3.10-slim

RUN apt -y update && apt -y upgrade
RUN apt -y install \
    # Necessary for pip install
    gcc g++ libc-dev \
    # For development and debug
    bash curl vim net-tools \
    # # For psycopg2 (postgresql client)
    # libpq-dev \
    # # For scikit-learn (scipy)
    # gfortran libopenblas-dev liblapack-dev \
    # # For opencv-python
    # libopencv-dev \
    && apt clean \
    && rm -rf /var/lib/apt/lists/*

# for updating python module
RUN pip install --upgrade pip \
    && pip install pipenv

ARG workdir="opt"
WORKDIR /${workdir}

# Install pip modules
COPY ./Pipfile ./
COPY ./Pipfile.lock ./

RUN pipenv sync
