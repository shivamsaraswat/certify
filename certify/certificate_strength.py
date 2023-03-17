import ssl
import socket
import certifi


def check_certificate_strength(hostname, port) -> dict:
    """
    Checks the strength of a certificate

    :param hostname: The hostname to check
    :type hostname: str
    :param port: The port to check
    :type port: int

    :return: The results of the validation
    :rtype: dict
    """

    strength = dict()

    try:
        context = ssl.create_default_context()
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(certifi.where())

        with socket.create_connection((hostname, port)) as sock:

            with context.wrap_socket(sock, server_hostname=hostname) as ssock:

                cipher = ssock.cipher()
                strength = {
                    "Cipher Suite" : str(cipher[0]),
                    "Cipher Strength" : str(cipher[2]) + " bits"
                }

    except Exception as e:
        print('Error:', e)

    return strength