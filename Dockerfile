# Build: docker build -t certify:latest .
# Run: docker run -it --rm certify -h

# Base Image
FROM python:3.12.4-alpine@sha256:63094abdaf49e046da9f6529ecd6ce4d853d9bfbf00a25c52bbbb68b3223b490

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