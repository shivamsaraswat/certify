# Certify

Certify is a powerful and easy-to-use Python tool designed to check the security of SSL/TLS certificates. It provides a range of options for analyzing certificates and identifying potential security risks, including the ability to display subject alternative names, subject common names, organization name, TLS version, cipher, certificate fingerprint hashes, JARM hash, certificate serial number, certificate pinning status, certificate authority verification, and certificate validity.

Certify also includes a number of features for identifying common certificate misconfigurations, such as expired, self-signed, mismatched, revoked, and untrusted certificates. The tool supports scanning individual hosts or lists of hosts, and allows for flexible output options, including the ability to write output to a file or display it in JSON format.

Whether you're a security researcher, network administrator, or just someone who wants to ensure the security of your online communications, Certify is an indispensable tool for analyzing SSL/TLS certificates and identifying potential security risks. With its powerful features and intuitive interface, it makes it easy to stay on top of the latest security threats and keep your systems safe and secure.

## Installation Through PIP
To install dependencies, use the following command:

```bash
pip install -r requirements.txt
```

To import certify as module, install it using the following command:
```bash
pip install certifycert
```

## Installation with Docker
This tool can also be used with [Docker](https://www.docker.com/). To set up the Docker environment, follow these steps (trying using with sudo, if you get any error):

```bash
docker build -t certify:latest .
```

## Using the Certify as command-line tool

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
usage: python3 certify [-h] [-v] [-d hostname] [-l file_path] [-p port] [-an] [-cn] [-on] [-tv] [-cipher] [-hash hash_name] [-jarm] [-sn] [-pin] [-av] [-vu] [-ex] [-ss] [-mm] [-re] [-un]
                       [-o file_path] [-j] [-silent]

Certify is a python tool designed to check the security of SSL/TLS certificates.

options:
  -h, --help            show this help message and exit
  -v, -version          display project version

INPUT:
  -d hostname, -host hostname
                        target host to scan (-d HOST1,HOST2)
  -l file_path, -list file_path
                        target list to scan (-l INPUT_FILE)
  -p port, -port port   target port to scan (default 443)

PROBES:
  -an                   display subject alternative names
  -cn                   display subject common names
  -on                   display subject organization name
  -tv, -tls-version     display used tls version
  -cipher               display used cipher
  -hash hash_name       display certificate fingerprint hashes (md5, sha1, sha224, sha256, sha384, sha512)
  -jarm                 display jarm hash
  -sn, -serial          display certificate serial number
  -pin                  display certificate pinning status
  -av, -authority-verification
                        display certificate authority verification (issued to, issued by)
  -vu, -valid-until     display certificate valid until

MISCONFIGURATIONS:
  -ex, -expired         display host with host expired certificate
  -ss, -self-signed     display host with self-signed certificate
  -mm, -mismatched      display host with mismatched certificate
  -re, -revoked         display host with revoked certificate
  -un, -untrusted       display host with untrusted certificate

OUTPUT:
  -o file_path, -output file_path
                        file to write output to
  -j, -json             display output in jsonline format
  -silent               display silent output

python3 certify -d example.com -tv
```

### Examples

#### Example 1:

```bash
> python3 certify -d cybersapien.tech -tv

 ██████╗███████╗██████╗ ████████╗██╗███████╗██╗   ██╗
██╔════╝██╔════╝██╔══██╗╚══██╔══╝██║██╔════╝╚██╗ ██╔╝
██║     █████╗  ██████╔╝   ██║   ██║█████╗   ╚████╔╝
██║     ██╔══╝  ██╔══██╗   ██║   ██║██╔══╝    ╚██╔╝
╚██████╗███████╗██║  ██║   ██║   ██║██║        ██║
 ╚═════╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝╚═╝        ╚═╝
     Coded with Love by Shivam Saraswat (@cybersapien)

cybersapien.tech:443 [TLSv1.3]
```

#### Example 2:

```bash
> python3 certify -l domains.txt -o cert.out -tv -on -cipher -hash sha512 -jarm -sn -pin -av -vu -silent
google.com:443 [TLSv1.3] [TLS_AES_256_GCM_SHA384] [256 bits] [20720863506ab451420d11d72c72d312674d61a822a642812ff8cde635ffd92e2fa6172d00fd0b033116b6d07e4b89c0412eae00af58deb0ddc5ecf5ac63b96a] [27d40d40d29d40d1dc42d43d00041d4689ee210389f4f6b4b5b1b93f92252d] [F27B612A054C603612DE2BB967B1F2CC] [Passed] [google.com] [GTS CA 1C3] [May 25, 2023 04:20:59 AM]
facebook.com:443 [Meta Platforms, Inc.] [TLSv1.3] [TLS_CHACHA20_POLY1305_SHA256] [256 bits] [6bc40449e06861f4d824fb941690c4b08688d2b720381a311af696a7b586f7630d52af11a17c3ebcbcb45d54b083a86d5d445a0782640835b58ff92b184b58b8] [27d27d27d0000001dc41d43d00041d286915b3b1e31b83ae31db5c5a16efc7] [01E6B342797813A1BE6E94AFC5457350] [Passed] [facebook.com] [DigiCert SHA2 High Assurance Server CA] [March 26, 2023 11:59:59 PM]
```

#### Example 3:

```bash
> python3 certify -d cybersapien.tech,facebook.com -an -cn

 ██████╗███████╗██████╗ ████████╗██╗███████╗██╗   ██╗
██╔════╝██╔════╝██╔══██╗╚══██╔══╝██║██╔════╝╚██╗ ██╔╝
██║     █████╗  ██████╔╝   ██║   ██║█████╗   ╚████╔╝
██║     ██╔══╝  ██╔══██╗   ██║   ██║██╔══╝    ╚██╔╝
╚██████╗███████╗██║  ██║   ██║   ██║██║        ██║
 ╚═════╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝╚═╝        ╚═╝
     Coded with Love by Shivam Saraswat (@cybersapien)

cybersapien.tech:443 [cybersapien.tech]
cybersapien.tech:443 [www.cybersapien.tech]
cybersapien.tech:443 [cybersapien.tech]

facebook.com:443 [facebook.com]
facebook.com:443 [facebook.net]
facebook.com:443 [fbcdn.net]
facebook.com:443 [fbsbx.com]
facebook.com:443 [m.facebook.com]
facebook.com:443 [messenger.com]
facebook.com:443 [xx.fbcdn.net]
facebook.com:443 [xy.fbcdn.net]
facebook.com:443 [xz.fbcdn.net]
facebook.com:443 [facebook.com]
```

## Using the Certify as module

### Examples

#### Example 1

```bash
from certify import Certify

print(Certify.is_expired('expired.badssl.com'))
```

#### Example 2

```bash
from certify import Certify

print(Certify.alternative_names('google.com'))
```

## Using the Docker Container

A typical run through Docker would look as follows:

```bash
docker run -it --rm certify -d hostname
```


