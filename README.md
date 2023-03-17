# Certify

"Certify" is a python tool designed to check the security of SSL/TLS certificates. The tool performs several tests to verify the validity and security of the certificate, including certificate validation, certificate revocation, certificate self-signed check, certificate expiration, certificate strength, certificate subject, certificate authority (CA) verification, and certificate pinning.

"Certify" allows security testers and administrators to quickly and easily verify the security of SSL/TLS certificates used by their websites or applications. It automates the testing process and provides detailed information on the results of each test, making it easy to identify and fix any security issues with the certificate.

## Installation Through PIP
To install dependencies, use the following command:

```bash
pip3 install -r requirements.txt
```

## Installation with Docker
This tool can also be used with [Docker](https://www.docker.com/). To set up the Docker environment, follow these steps (trying using with sudo, if you get any error):

```bash
docker build -t certify:latest .
```

## Using the Certify

To run the Certify on a hostname, provide the hostname with the -d flag:

```bash
python3 certify -d example.com
```

For an overview of all commands use the following command:

```bash
python3 certify -h
```

The output shown below are the latest supported commands.

```bash
 ██████╗███████╗██████╗ ████████╗██╗███████╗██╗   ██╗
██╔════╝██╔════╝██╔══██╗╚══██╔══╝██║██╔════╝╚██╗ ██╔╝
██║     █████╗  ██████╔╝   ██║   ██║█████╗   ╚████╔╝
██║     ██╔══╝  ██╔══██╗   ██║   ██║██╔══╝    ╚██╔╝
╚██████╗███████╗██║  ██║   ██║   ██║██║        ██║
 ╚═════╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝╚═╝        ╚═╝   
     Coded with Love by Shivam Saraswat (@cybersapien)

usage: python3 certify [-h] -d HOSTNAME [-o file_path] [-v]

Checks the security of a certificate

options:
  -h, --help            show this help message and exit
  -d HOSTNAME, -host HOSTNAME, --hostname HOSTNAME
                        The hostname to check
  -o file_path, --output file_path
                        The output file to write to
  -v, --version         show program's version number and exit

python3 certify -d example.com -o cert.out
```

## Using the Docker Container

A typical run through Docker would look as follows:

```bash
docker run -it --rm certify -d example.com
```
