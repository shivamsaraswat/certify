from ocspchecker import ocspchecker


def check_certificate_revocation(hostname) -> bool:
    """
    Checks if a certificate is revoked

    :param hostname: The hostname to check
    :type hostname: str

    :return: True if the certificate is not revoked, False otherwise
    :rtype: bool
    """

    try:
        ocsp_request = ocspchecker.get_ocsp_status(hostname)
        if ocsp_request and 'OCSP Status: GOOD' in ocsp_request:
            return True
        else:
            return False

    except Exception:
        return False
