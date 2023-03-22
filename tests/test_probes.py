from certify.probes.jarm_hash import get_jarm_hash
from certify.probes.calculate_hash import get_hashes
from certify.probes.tls_version import get_tls_version
from certify.probes.common_name import get_common_name
from certify.probes.serial_number import get_serial_number
from certify.probes.alternative_names import get_alternative_names
from certify.probes.organization_name import get_organization_name
from certify.probes.certificate_pinning import check_certificate_pinning
from certify.probes.certificate_strength import check_certificate_strength
from certify.probes.certificate_authority_verification import check_authority_verification


def test_alternative_names():

    alt_names = get_alternative_names("cybersapien.tech", 443)

    assert sorted(alt_names) == sorted(["www.cybersapien.tech", "cybersapien.tech"])

def test_calculate_hash():

    md5_hash = get_hashes("cybersapien.tech", 443, hash_name="md5")
    all_hashes = get_hashes("cybersapien.tech", 443, all_hash=True)

    assert md5_hash == "e0e5e19c9556180f6a387b793a29652b"
    assert all_hashes == {'md5': 'e0e5e19c9556180f6a387b793a29652b', 'sha1': '1dcda5d8e32a021c6a42420902c5f46ded7041d2', 'sha224': '621370f071dc746763733c6894d9c3ba2b3b9e3685c18ab019393ac9', 'sha256': 'd0ed9007bfb23caabf88bca24f94835db8010884d015b1d7b86ed896f1552970', 'sha384': '79e0961d6b1880bd92f52b3137bc41f13333e55a5fb5f4b59a8de2aceb97d89f218e65038d3c40fa20013f98d969497e', 'sha512': '589d734683f02b353e9c37c500a85b3cbde2a9de7ddf68f31885968e8558864bda07b6b523a332e7d081383109e833299aca4c71219d591e8a11cbe3b4c971db'}

def test_certificate_authority_verification():

    issued_to, issued_by = check_authority_verification("cybersapien.tech", 443)

    assert issued_to == "cybersapien.tech"
    assert issued_by == "R3"

def test_certificate_pinning():

    pinning = check_certificate_pinning("cybersapien.tech")

    assert pinning == True

def test_certificate_strength():

    cipher, key_size = check_certificate_strength("cybersapien.tech", 443)

    assert cipher == "TLS_AES_256_GCM_SHA384"
    assert key_size == "256 bits"

def test_common_name():

    common_name = get_common_name("cybersapien.tech", 443)

    assert common_name == "cybersapien.tech"

def test_jarm_hash():

    jarm_hash = get_jarm_hash("cybersapien.tech", 443)

    assert jarm_hash == "29d29d00029d29d00042d42d0000002059a3b916699461c5923779b77cf06b"

def test_organization_name():

    organization_name = get_organization_name("facebook.com", 443)

    assert organization_name == "Meta Platforms, Inc."

def test_serial_number():

    serial_number = get_serial_number("cybersapien.tech", 443)

    assert serial_number == "04BB7AAEBF3692C2F5887A7E0C389BB6513F"

def test_tls_version():

    tls_version, _ = get_tls_version("cybersapien.tech", 443)

    assert tls_version == "TLSv1.3"
