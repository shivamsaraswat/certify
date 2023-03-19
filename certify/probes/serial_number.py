import ssl
import socket


def get_serial_number(hostname, port) -> str:
    """
    Gets the serial number of a certificate

    :param hostname: The hostname to check
    :type hostname: str
    :param port: The port to check
    :type port: int

    :return: The serial number of the certificate
    :rtype: str
    """

    try:
        with ssl.create_default_context().wrap_socket(socket.socket(), server_hostname=hostname) as ssock:
            ssock.connect((hostname, port))
            cert = ssock.getpeercert()
            return cert['serialNumber']

    except Exception:
        return ""

