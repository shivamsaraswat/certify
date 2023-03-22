import ssl
from OpenSSL import crypto
from datetime import datetime


def check_certificate_expiration(hostname, port) -> tuple[bool, str]:
    """
    Checks if a certificate is expired

    :param hostname: The hostname to check
    :type hostname: str
    :param port: The port to check
    :type port: int

    :return: True if the certificate is not expired, False otherwise
    :rtype: tuple[bool, str]
    """

    try:
        cert = ssl.get_server_certificate((hostname, port))
        x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert)

        if x509.has_expired():
            return False, "Certificate has expired."
        else:
            expiration_datetime = datetime.strptime(x509.get_notAfter().decode(), "%Y%m%d%H%M%SZ")
            expiration_formatted = expiration_datetime.strftime("%B %d, %Y %I:%M:%S %p")
            return True, expiration_formatted

    except Exception:
        return "None", "Invalid Certificate"
