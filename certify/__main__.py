import json
import argparse
import certificate_subject
import certificate_pinning
import certificate_strength
import certificate_validation
import certificate_revocation
import certificate_expiration
import certificate_self_signed
import certificate_authority_verification
from termcolor import colored


def logo() -> None:
    print(colored("""
 ██████╗███████╗██████╗ ████████╗██╗███████╗██╗   ██╗
██╔════╝██╔════╝██╔══██╗╚══██╔══╝██║██╔════╝╚██╗ ██╔╝
██║     █████╗  ██████╔╝   ██║   ██║█████╗   ╚████╔╝
██║     ██╔══╝  ██╔══██╗   ██║   ██║██╔══╝    ╚██╔╝
╚██████╗███████╗██║  ██║   ██║   ██║██║        ██║
 ╚═════╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝╚═╝        ╚═╝   """))
    print(colored('     Coded with Love by Shivam Saraswat (@cybersapien)\n', 'green', attrs=['bold']))


def parse_arguments() -> argparse.Namespace:
    """
    Parses the arguments passed to the script

    :return: The arguments
    :rtype: argparse.Namespace
    """

    parser = argparse.ArgumentParser(prog='python3 certify', description='Checks the security of a certificate', epilog='python3 certify -d example.com -o cert.out')
    parser.add_argument('-d',  '-host', '--hostname', type=str, required=True, help='The hostname to check')
    parser.add_argument('-o', '--output', type=argparse.FileType('w'), metavar='file_path', action='store', dest='output', help='The output file to write to')
    parser.add_argument('-v', '--version', action='version', version='1.0')
    args = parser.parse_args()

    return args


if __name__ == '__main__':

    logo()

    args = parse_arguments()
    hostname = args.hostname
    output = args.output
    port = 443

    out_dict = dict()

    # Check if the certificate is self-signed
    if certificate_self_signed.check_certificate_self_signed(hostname, port):
        out_dict['Self-Signed'] = 'Yes'
    else:
        out_dict['Self-Signed'] = 'No'
    
    # Check if the certificate is valid
    valid, version = certificate_validation.validate_certificate(hostname, port)
    out_dict['Valid'] = valid

    if valid:
        out_dict['Version'] = version

        # Check if the certificate is revoked
        if certificate_revocation.check_certificate_revocation(hostname):
            out_dict['Revoked'] = 'No'
        else:
            out_dict['Revoked'] = 'Yes'
            out_dict['Valid'] = 'No'

        # Check if the certificate is expired
        expired_bool, expired_str = certificate_expiration.check_certificate_expiration(hostname, port)
        if expired_bool:
            out_dict['Expired'] = 'No'
            out_dict['Valid Until'] = expired_str
        else:
            out_dict['Expired'] = 'Yes'

        # Check the certificate strength
        out_dict.update(certificate_strength.check_certificate_strength(hostname, port))

        # Check the certificate subject
        out_dict.update(certificate_subject.check_certificate_subject(hostname, port))

        # Check the certificate authority verification
        out_dict.update(certificate_authority_verification.check_authority_verification(hostname, port))

        # Check if the certificate passes certificate pinning
        if certificate_pinning.check_certificate_pinning(hostname):
            out_dict['Certificate Pinning'] = 'Passed'
        else:
            out_dict['Certificate Pinning'] = 'Failed'

        print("Certificate Information:")
        print(json.dumps(out_dict, indent=4))

    else:
        print("Certificate Information:")
        out_dict['Error'] = version
        print(json.dumps(out_dict, indent=4))

    # Write to the output file
    if output:
        with open(output.name, 'w') as f:
            json.dump(out_dict, f, indent=4)
