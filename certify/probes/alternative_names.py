import ssl
import socket


def get_alternative_names(hostname, port) -> list:
    """
    Get the alternative names from the certificate

    :param hostname: Hostname to connect to
    :type hostname: str
    :param port: Port to connect to
    :type port: int

    :return: List of alternative names
    :rtype: list
    """

    alt_names = set()

    try:

        with ssl.create_default_context().wrap_socket(socket.socket(), server_hostname=hostname) as ssock:
            ssock.connect((hostname, port))
            cert = ssock.getpeercert()
            for alt_name in cert['subjectAltName']:
                if alt_name[0] == 'DNS':
                    alt = alt_name[1].strip('*')
                    if alt.startswith('.'):
                        alt = alt[1:]
                        alt_names.add(alt)
                    else:
                        alt_names.add(alt)

            return sorted(alt_names)

    except Exception:
        return []
