import ssl
import socket
import certifi


def get_tls_version(hostname, port) -> str:
    """
    Checks the TLS version used by the server

    :param hostname: The hostname to check
    :type hostname: str
    :param port: The port to check
    :type port: int

    :return: The TLS version used by the server
    :rtype: str
    """

    try:
        context = ssl.create_default_context()
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(certifi.where())

        with socket.create_connection((hostname, port)) as sock:

            with context.wrap_socket(sock, server_hostname=hostname) as ssock:

                return ssock.version()

    except Exception as e:
        return ""
