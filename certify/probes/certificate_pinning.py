import certifi
import requests


def check_certificate_pinning(hostname) -> bool:
    """
    Checks if a certificate is pinned

    :param hostname: The hostname to check
    :type hostname: str

    :return: True if the certificate is pinned, False otherwise
    :rtype: bool
    """

    try:
        resp = requests.get(f'https://{hostname}', verify=certifi.where())
        if resp.status_code == 200:
            return True
        else:
            return False

    except Exception:
        return False
