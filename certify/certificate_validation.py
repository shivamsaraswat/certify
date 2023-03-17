import ssl
import socket
import certifi


def validate_certificate(hostname, port) -> str:
    """
    Validates the certificate of a given hostname

    :param hostname: The hostname to check
    :type hostname: str
    :param port: The port to check
    :type port: int

    :return: The results of the validation
    :rtype: str
    """

    try:
        context = ssl.create_default_context()
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(certifi.where())

        with socket.create_connection((hostname, port)) as sock:

            with context.wrap_socket(sock, server_hostname=hostname) as ssock:

                return True, ssock.version()

    except Exception as e:
        return False, str(e)
