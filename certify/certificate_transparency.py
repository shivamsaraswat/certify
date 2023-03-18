# import ssl
# from cryptography import x509
# from OpenSSL import crypto

# # Specify the hostname name to check
# hostname = 'facebook.com'

# # Extract the leaf certificate from the chain
# cert = ssl.get_server_certificate((hostname, 443))
# x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert)

# # Extract the certificate extensions
# extensions = x509.get_extension_count()

# # # Check if the certificate has the Signed Certificate Timestamp (SCT) extension
# # if extensions.get_extension_for_oid(x509.oid.ExtensionOID.EXTENDED_KEY_USAGE).value.native == ['1.3.6.1.5.5.7.3.1']:
# #     print('Certificate Transparency (CT) check passed')
# # else:
# #     print('Certificate Transparency (CT) check failed')



# import subprocess

# # Replace example.com with the domain name of the website you want to check
# domain = "example.com"

# # Run the openssl s_client command and capture the output
# with subprocess.Popen(["openssl", "s_client", "-connect", f"{domain}:443", "-showcerts"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc1:

#     # Run the openssl x509 command on the output of the s_client command and capture the output
#     with subprocess.Popen(["openssl", "x509", "-noout", "-text"], stdin=proc1.stdout, stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc2:
        
#         # Read the output of the x509 command line by line
#         for line in proc2.stdout:
#             if "Certificate Transparency" in line.decode():
#                 print(line.decode().strip())


