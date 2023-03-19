import ssl
from OpenSSL import crypto


def get_common_name(hostname, port) -> str:
    """
    Gets the common name of a certificate

    :param hostname: The hostname to check
    :type hostname: str
    :param port: The port to check
    :type port: int

    :return: The common name of the certificate
    :rtype: str
    """

    try:
        cert = ssl.get_server_certificate((hostname, port))
        x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert)

        return x509.get_subject().CN.strip('*.')

    except Exception:
        return ""

