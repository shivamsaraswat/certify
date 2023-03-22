import argparse

def parse_arguments() -> argparse.Namespace:
    """
    Parses the arguments passed to the script

    :return: The arguments
    :rtype: argparse.Namespace
    """

    parser = argparse.ArgumentParser(prog='python3 certify', description='certify is a python tool designed to check the security of SSL/TLS certificates.', epilog='python3 certify -d example.com -tv')
    parser.add_argument('-v', '-version', action='version', version='Current version: v0.1.0', help='display project version')

    group1 = parser.add_argument_group('INPUT')
    group1.add_argument('-d', '-host', type=str, metavar='hostname', help='target host to scan (-d HOST1,HOST2)')
    group1.add_argument('-l', '-list', metavar='file_path', help='target list to scan (-l INPUT_FILE)')
    group1.add_argument('-p', '-port', type=int, metavar='port', action='store', dest='port', default=443, help='target port to scan (default 443)')

    group2 = parser.add_argument_group('PROBES')
    group2.add_argument('-an', action='store_true', help='display subject alternative names')
    group2.add_argument('-cn', action='store_true', help='display subject common names')
    group2.add_argument('-on', action='store_true', help='display subject organization name')
    group2.add_argument('-tv', '-tls-version', action='store_true', help='display used tls version')
    group2.add_argument('-cipher', action='store_true', help='display used cipher')
    group2.add_argument('-hash', type=str, metavar='hash_name', help='display certificate fingerprint hashes (md5, sha1, sha224, sha256, sha384, sha512)')
    group2.add_argument('-jarm', action='store_true', help='display jarm hash')
    group2.add_argument('-sn', '-serial', action='store_true', help='display certificate serial number')
    group2.add_argument('-pin', action='store_true', help='display certificate pinning status')
    group2.add_argument('-av', '-authority-verification', action='store_true', help='display certificate authority verification (issued to, issued by)')
    group2.add_argument('-vu', '-valid-until', action='store_true', help='display certificate valid until')

    group3 = parser.add_argument_group('MISCONFIGURATIONS')
    group3.add_argument('-ex', '-expired', action='store_true', help='display host with host expired certificate')
    group3.add_argument('-ss', '-self-signed', action='store_true', help='display host with self-signed certificate')
    group3.add_argument('-mm', '-mismatched', action='store_true', help='display host with mismatched certificate')
    group3.add_argument('-re', '-revoked', action='store_true', help='display host with revoked certificate')
    group3.add_argument('-un', '-untrusted', action='store_true', help='display host with untrusted certificate')

    group4 = parser.add_argument_group('OUTPUT')
    group4.add_argument('-o', '-output', type=argparse.FileType('w'), metavar='file_path', action='store', dest='output', help='file to write output to')
    group4.add_argument('-j', '-json', action='store_true', help='display output in jsonline format')
    group4.add_argument('-silent', action='store_true', help='display silent output')

    args = parser.parse_args()

    return args

