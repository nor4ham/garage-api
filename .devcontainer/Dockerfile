FROM mcr.microsoft.com/vscode/devcontainers/python:0-3.11

WORKDIR /workspaces/garage-api

COPY ./requirements.txt requirements.txt
COPY ./requirements-dev.txt requirements-dev.txt


RUN pip install --no-cache-dir \
    -r requirements-dev.txt \
    && rm -rf /tmp/pip-tmp