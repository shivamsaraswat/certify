# Build: docker build -t certify:latest .
# Run: docker run -it --rm certify -h

# Base Image
FROM python:3.11.2-alpine@sha256:4b4078a3ab81edc2f5725cd42b065beaeeb4f9be3b4b1e3b4cf11dd6ae9720d3

# Maintainer
LABEL maintainer="Shivam Saraswat <thecybersapien@protonmail.com>"
LABEL description="Certify is a python tool designed to check the security of SSL/TLS certificates."

# Install OS Dependencies
RUN apk update && apk upgrade && apk add --no-cache bash gcc libffi-dev musl-dev curl

# Set Work Directory
WORKDIR /usr/src/app
# Copy Project
COPY . .

# setup virtualenv
RUN python3 -m venv venv
RUN . venv/bin/activate

# Install Project Dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Start with console arguments passed to docker run
ENTRYPOINT ["python3", "certify"]