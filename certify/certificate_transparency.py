import ssl
from cryptography import x509
from OpenSSL import crypto

# Specify the hostname name to check
hostname = 'facebook.com'

# Extract the leaf certificate from the chain
cert = ssl.get_server_certificate((hostname, 443))
x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert)

# Extract the certificate extensions
extensions = x509.get_extension_count()

# # Check if the certificate has the Signed Certificate Timestamp (SCT) extension
# if extensions.get_extension_for_oid(x509.oid.ExtensionOID.EXTENDED_KEY_USAGE).value.native == ['1.3.6.1.5.5.7.3.1']:
#     print('Certificate Transparency (CT) check passed')
# else:
#     print('Certificate Transparency (CT) check failed')
