import ssl
from OpenSSL import crypto


def check_certificate_subject(hostname, port) -> str:
    """
    Checks the subject of a certificate

    :param hostname: The hostname to check
    :type hostname: str
    :param port: The port to check
    :type port: int

    :return: The subject of the certificate
    :rtype: str
    """

    try:
        cert = ssl.get_server_certificate((hostname, port))
        cert = ssl.DER_cert_to_PEM_cert(ssl.PEM_cert_to_DER_cert(cert))
        x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert)
        return {"Certificate Subject:" : str(x509.get_subject().CN)}

    except Exception as e:
        print('Error:', e)
        return {}