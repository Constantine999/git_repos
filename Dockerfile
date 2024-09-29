FROM python:3.12-slim

WORKDIR /github_repos

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY github_repos .