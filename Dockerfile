FROM python:3.9
LABEL fileversion=v0.01

ARG RUN_ENVIRONMENT
ENV RUN_ENVIRONMENT=${RUN_ENVIRONMENT}
ENV ENV=${RUN_ENVIRONMENT}

WORKDIR /app/

COPY . .

RUN pip install -r requirements.txt --quiet
