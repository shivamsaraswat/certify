from certify.misconfigurations.certificate_trust import check_certificate_trust
from certify.misconfigurations.certificate_revocation import check_certificate_revocation
from certify.misconfigurations.certificate_expiration import check_certificate_expiration
from certify.misconfigurations.certificate_mismatched import check_certificate_mismatched
from certify.misconfigurations.certificate_self_signed import check_certificate_self_signed


def test_is_expired():

    expired, _ = check_certificate_expiration("expired.badssl.com", 443)
    assert expired == False

def test_is_mismatched():

    mismatched = check_certificate_mismatched("google.com", 443)
    assert mismatched == True

def test_is_revoked():

    revoked = check_certificate_revocation("cybersapien.tech")
    assert revoked == True

def test_is_self_signed():

    self_signed = check_certificate_self_signed("self-signed.badssl.com", 443)
    assert self_signed == True

def test_is_trusted():

    trusted = check_certificate_trust("cybersapien.tech")
    assert trusted == True
