import ssl
import OpenSSL


def check_certificate_self_signed(hostname, port) -> bool:
    """
    Checks if a certificate is self-signed

    :param hostname: The hostname to check
    :type hostname: str
    :param port: The port to check
    :type port: int

    :return: True if the certificate is self-signed, False otherwise
    :rtype: bool
    """

    try:
        cert = ssl.get_server_certificate((hostname, port))
        x509 = OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert)
        issuer = dict(x509.get_issuer().get_components())
        subject = dict(x509.get_subject().get_components())

        issuer_dict = dict()
        subject_dict = dict()

        for key, value in issuer.items():
            # Decode the value if it's a bytes object
            if isinstance(value, bytes):
                value = value.decode()
            # Add the key-value pair
            issuer_dict[key.decode()] = value

        for key, value in subject.items():
            # Decode the value if it's a bytes object
            if isinstance(value, bytes):
                value = value.decode()
            # Add the key-value pair
            subject_dict[key.decode()] = value

        if issuer_dict['CN'] == subject_dict['CN']:
            return True
        else:
            return False

    except Exception:
        return False
