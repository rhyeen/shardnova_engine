FROM python:alpine

MAINTAINER rhyeen@gmail.com

WORKDIR /home/default

# Update Apt
RUN apt-get update

RUN pip install --upgrade pip
# Dependencies for log_manager.py.
## Once in a blue-moon there is an SSLError that occurs with TCP handshakes.
## Installing pyopenssl ndg-httpsclient is meant to remedy this; however, according to this thread:
## https://github.com/requests/requests/issues/3006 it seems to only be a MacOS issue, which wouldn't explain it.
RUN pip install PyMySQL requests pyopenssl ndg-httpsclient pyjwt

# Get everything in current directory that's not in .dockerignore
COPY ./ /home/default

## Set env vars
# Not Secret
ENV MYSQL_HOST 'shardrealms.com'
ENV MYSQL_USER 'sr_creation_dev'
ENV MYSQL_DATABASE 'sr_creation_dev'
ENV MYSQL_PORT '3306'

# Secret
ENV MYSQL_PASSWORD 'not_password'

CMD ["python", "/home/default/src/engine/runner.py"]
