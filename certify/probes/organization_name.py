import ssl
import OpenSSL


def get_organization_name(hostname, port) -> str:
    """
    Gets the organization name of a certificate

    :param hostname: The hostname to check
    :type hostname: str
    :param port: The port to check
    :type port: int

    :return: The organization name of the certificate
    :rtype: str
    """

    try:
        cert = ssl.get_server_certificate((hostname, port))
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)

        return x509.get_subject().O

    except Exception:
        return ""
