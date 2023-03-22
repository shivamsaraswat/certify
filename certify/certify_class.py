from .probes.jarm_hash import get_jarm_hash
from .probes.calculate_hash import get_hashes
from .probes.tls_version import get_tls_version
from .probes.common_name import get_common_name
from .probes.serial_number import get_serial_number
from .probes.alternative_names import get_alternative_names
from .probes.organization_name import get_organization_name
from .probes.certificate_pinning import check_certificate_pinning
from .probes.certificate_strength import check_certificate_strength
from .probes.certificate_authority_verification import check_authority_verification

from .misconfigurations.certificate_trust import check_certificate_trust
from .misconfigurations.certificate_revocation import check_certificate_revocation
from .misconfigurations.certificate_expiration import check_certificate_expiration
from .misconfigurations.certificate_mismatched import check_certificate_mismatched
from .misconfigurations.certificate_self_signed import check_certificate_self_signed


class Certify:

    def __init__(self) -> None:
        pass

    @staticmethod
    def is_expired(hostname, port=443) -> tuple[bool, str]:
        """
        Check if the certificate is expired or not.

        :param hostname: Hostname of the website
        :type hostname: str
        :param port: Port of the website, defaults to 443
        :type port: int, optional

        :return: True if the certificate is expired, False if not
        :rtype: bool
        """

        expired_bool, reason_or_valid_until = check_certificate_expiration(hostname, port)

        if expired_bool == False:
            return True, reason_or_valid_until
        elif expired_bool == True:
            return False, reason_or_valid_until

        return True, reason_or_valid_until

    @staticmethod
    def is_mismatched(hostname, port=443) -> bool:
        """
        Check if the certificate is mismatched or not.

        :param hostname: Hostname of the website
        :type hostname: str
        :param port: Port of the website, defaults to 443
        :type port: int, optional

        :return: True if the certificate is mismatched, False if not
        :rtype: bool
        """

        mismatched_bool = check_certificate_mismatched(hostname, port)

        if mismatched_bool:
            return True

        return False

    @staticmethod
    def is_revoked(hostname) -> bool:
        """
        Check if the certificate is revoked or not.

        :param hostname: Hostname of the website
        :type hostname: str

        :return: True if the certificate is revoked, False if not
        :rtype: bool
        """

        revoked_bool = check_certificate_revocation(hostname)

        if not revoked_bool:
            return True

        return False

    @staticmethod
    def is_self_signed(hostname, port=443) -> bool:
        """
        Check if the certificate is self-signed or not.

        :param hostname: Hostname of the website
        :type hostname: str
        :param port: Port of the website, defaults to 443
        :type port: int, optional

        :return: True if the certificate is self-signed, False if not
        :rtype: bool
        """

        if check_certificate_self_signed(hostname, port):
            return True

        return False

    @staticmethod
    def is_trusted(hostname) -> bool:
        """
        Check if the certificate is trusted or not.

        :param hostname: Hostname of the website
        :type hostname: str

        :return: True if the certificate is trusted, False if not
        :rtype: bool
        """

        trusted_bool = check_certificate_trust(hostname)

        if not trusted_bool:
            return False

        return True

    @staticmethod
    def alternative_names(hostname, port=443) -> list[str]:
        """
        Get the alternative names of the certificate.

        :param hostname: Hostname of the website
        :type hostname: str
        :param port: Port of the website, defaults to 443
        :type port: int, optional

        :return: List of alternative names
        :rtype: list[str]
        """

        alt_names = get_alternative_names(hostname, port)

        return alt_names

    @staticmethod
    def calculate_hash(hostname, port=443, hash_name=None, all_hash=False) -> list[str] or str:
        """
        Calculate the hash of the certificate.

        :param hostname: Hostname of the website
        :type hostname: str
        :param port: Port of the website, defaults to 443
        :type port: int, optional
        :param hash_name: Name of the hash, defaults to None
        :type hash_name: str, optional
        :param all_hash: Return all the hashes, defaults to False
        :type all_hash: bool, optional

        :return: Hash of the certificate
        :rtype: str
        """

        hashes = get_hashes(hostname, port, hash_name, all_hash)

        return hashes

    @staticmethod
    def authority_verification_details(hostname, port=443) -> dict[str, str]:
        """
        Get the details of the certificate authority.

        :param hostname: Hostname of the website
        :type hostname: str
        :param port: Port of the website, defaults to 443
        :type port: int, optional

        :return: Details of the certificate authority
        :rtype: dict[str, str]
        """

        issued_to, issued_by = check_authority_verification(hostname, port)

        return {"issued_to": issued_to, "issued_by": issued_by}

    @staticmethod
    def is_pinning_test_passed(hostname) -> bool:
        """
        Check if the certificate pinning test is passed or not.

        :param hostname: Hostname of the website
        :type hostname: str

        :return: True if the certificate pinning test is passed, False if not
        :rtype: bool
        """

        if check_certificate_pinning(hostname):
            return True

        return False

    @staticmethod
    def certificate_strength(hostname, port=443) -> dict[str, str]:
        """
        Get the strength of the certificate.

        :param hostname: Hostname of the website
        :type hostname: str
        :param port: Port of the website, defaults to 443
        :type port: int, optional

        :return: Strength of the certificate
        :rtype: dict[str, str]
        """

        cipher, key_size = check_certificate_strength(hostname, port)

        return {"cipher": cipher, "key_size": key_size}

    @staticmethod
    def common_name(hostname, port=443) -> str:
        """
        Get the common name of the certificate.

        :param hostname: Hostname of the website
        :type hostname: str
        :param port: Port of the website, defaults to 443
        :type port: int, optional

        :return: Common name of the certificate
        :rtype: str
        """

        cname = get_common_name(hostname, port)

        return cname

    @staticmethod
    def jarm_hash(hostname, port=443) -> str:
        """
        Get the JARM hash of the certificate.

        :param hostname: Hostname of the website
        :type hostname: str
        :param port: Port of the website, defaults to 443
        :type port: int, optional

        :return: JARM hash of the certificate
        :rtype: str
        """

        jarm_hash = get_jarm_hash(hostname, port)

        return jarm_hash

    @staticmethod
    def organization_name(hostname, port=443) -> str:
        """
        Get the organization name of the certificate.

        :param hostname: Hostname of the website
        :type hostname: str
        :param port: Port of the website, defaults to 443
        :type port: int, optional

        :return: Organization name of the certificate
        :rtype: str
        """

        oname = get_organization_name(hostname, port)

        return oname

    @staticmethod
    def serial_number(hostname, port=443) -> str:
        """
        Get the serial number of the certificate.

        :param hostname: Hostname of the website
        :type hostname: str
        :param port: Port of the website, defaults to 443
        :type port: int, optional

        :return: Serial number of the certificate
        :rtype: str
        """

        snum = get_serial_number(hostname, port)

        return snum

    @staticmethod
    def tls_version(hostname, port=443) -> str:
        """
        Get the TLS version of the certificate.

        :param hostname: Hostname of the website
        :type hostname: str
        :param port: Port of the website, defaults to 443
        :type port: int, optional

        :return: TLS version of the certificate
        :rtype: str
        """

        tlsv, _ = get_tls_version(hostname, port)

        return tlsv
