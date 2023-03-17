import ssl
import socket
import certifi


def check_authority_verification(hostname, port) -> dict:
    """
    Checks the authority verification of a certificate

    :param hostname: The hostname to check
    :type hostname: str
    :param port: The port to check
    :type port: int

    :return: The results of the validation
    :rtype: dict
    """

    authority_details = dict()

    try:
        context = ssl.create_default_context()
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(certifi.where())

        with socket.create_connection((hostname, port)) as sock:

            with context.wrap_socket(sock, server_hostname=hostname) as ssock:

                cert = ssock.getpeercert()
                subject = dict(x[0] for x in cert['subject'])
                issued_to = subject['commonName']
                issuer = dict(x[0] for x in cert['issuer'])
                issued_by = issuer['commonName']

                authority_details['Certificate Issued To'] = issued_to
                authority_details['Certificate Issued By'] = issued_by

    except Exception as e:
        print('Error:', e)

    return authority_details