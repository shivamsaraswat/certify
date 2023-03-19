import asyncio
from jarm.scanner.scanner import Scanner


def get_jarm_hash(hostname, port) -> str:
    """
    Gets the JARM hash of a certificate

    :param hostname: The hostname to check
    :type hostname: str
    :param port: The port to check
    :type port: int

    :return: The JARM hash of the certificate
    :rtype: str
    """

    try:
        return asyncio.run(Scanner.scan_async(hostname, port))[0]

    except Exception:
        return ""
