import socket
import ssl


def check_certificate_mismatched(hostname, port) -> bool:
    """
    Check if the certificate is mismatched with the hostname.

    :param hostname: The hostname to check
    :type hostname: str
    :param port: The port to check
    :type port: int

    :return: True if the certificate is mismatched, False otherwise
    :rtype: bool
    """

    try:
        # create a socket connection to the hostname and port
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((hostname, port))

        # wrap the socket in an SSL context
        context = ssl.create_default_context()
        ssock = context.wrap_socket(s, server_hostname=hostname)

        # check if the certificate is mismatched
        cert = ssock.getpeercert()
        if not hostname == cert['subjectAltName'][0][1]:
            return True
        else:
            return False

    except Exception:
        return False

