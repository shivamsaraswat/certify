import sys
import json as jsonlib
from termcolor import colored
from input_args import parse_arguments
from probes.alternative_names import get_alternative_names
from probes.common_name import get_common_name
from probes.calculate_hash import get_hashes
from probes.jarm_hash import get_jarm_hash
from probes.serial_number import get_serial_number
from probes.organization_name import get_organization_name
from probes.tls_version import get_tls_version
from probes.certificate_pinning import check_certificate_pinning
from probes.certificate_strength import check_certificate_strength
from probes.certificate_authority_verification import check_authority_verification
from misconfigurations.certificate_revocation import check_certificate_revocation
from misconfigurations.certificate_expiration import check_certificate_expiration
from misconfigurations.certificate_self_signed import check_certificate_self_signed
from misconfigurations.certificate_mismatched import check_certificate_mismatched
from misconfigurations.certificate_trust import check_certificate_trust


def logo() -> None:
    print(colored("""
 ██████╗███████╗██████╗ ████████╗██╗███████╗██╗   ██╗
██╔════╝██╔════╝██╔══██╗╚══██╔══╝██║██╔════╝╚██╗ ██╔╝
██║     █████╗  ██████╔╝   ██║   ██║█████╗   ╚████╔╝
██║     ██╔══╝  ██╔══██╗   ██║   ██║██╔══╝    ╚██╔╝
╚██████╗███████╗██║  ██║   ██║   ██║██║        ██║
 ╚═════╝╚══════╝╚═╝  ╚═╝   ╚═╝   ╚═╝╚═╝        ╚═╝   """))
    print(colored('     Coded with Love by Shivam Saraswat (@cybersapien)\n', 'green', attrs=['bold']))


def json_out(hostname, port) -> None:

    out_dict = dict()

    # Check if the certificate is self-signed
    if check_certificate_self_signed(hostname, port):
        out_dict['Self-Signed'] = 'Yes'
    else:
        out_dict['Self-Signed'] = 'No'

    # Check if the certificate is valid
    expired_bool, expired_str = check_certificate_expiration(hostname, port)
    if not expired_bool:
        out_dict['Valid'] = 'No'
        out_dict['Expired'] = 'Yes'

    if expired_bool:
        version = get_tls_version(hostname, port)
        out_dict['Version'] = version

        # Check if the certificate is revoked
        if check_certificate_revocation(hostname):
            out_dict['Revoked'] = 'No'
        else:
            out_dict['Revoked'] = 'Yes'
            out_dict['Valid'] = 'No'

        # Add expiration status and date
        if expired_bool:
            out_dict['Expired'] = 'No'
            out_dict['Valid Until'] = expired_str

        # Check the certificate strength
        cipher, strength = check_certificate_strength(hostname, port)
        out_dict['Cipher Suite'] = cipher
        out_dict['Cipher Strength'] = strength

        # Check the certificate subject
        cname = get_common_name(hostname, port)
        out_dict['Common Name'] = cname

        # Check the certificate authority verification
        issued_to, issued_by = (check_authority_verification(hostname, port))
        out_dict['Certificate Issued To'] = issued_to
        out_dict['Certificate Issued By'] = issued_by

        # Check if the certificate passes certificate pinning
        if check_certificate_pinning(hostname):
            out_dict['Certificate Pinning'] = 'Passed'
        else:
            out_dict['Certificate Pinning'] = 'Failed'

        print("Certificate Information:")
        print(jsonlib.dumps(out_dict, indent=4))

    else:
        print("Certificate Information:")
        out_dict['Error'] = version
        print(jsonlib.dumps(out_dict, indent=4))

    # Write to the output file
    if output:
        with open(output.name, 'w') as f:
            jsonlib.dump(out_dict, f, indent=4)

if __name__ == '__main__':

    args = parse_arguments()
    hostname = args.d
    port = args.port
    output = args.output
    silent = args.silent

    if not silent:
        logo()

    probes_specified = args.on or args.j or args.tv or args.cipher or args.hash or args.jarm or args.sn or args.pin or args.av or args.ex or args.ss or args.mm or args.re or args.un
    if (args.an or args.cn) and probes_specified:
        print(colored('[-] Error: -an and -cn cannot be used with other probe flags.', 'red', attrs=['bold']))
        sys.exit(0)

    expired_bool, expired_str = check_certificate_expiration(hostname, port)
    
    # display certificate expiration status
    if args.ex:
        print(hostname + ":" + str(port) ,end=' ')
        if not expired_bool:
            print(colored('[Expired]', 'red', attrs=['bold']))
            sys.exit(0)

    # display subject alternative names
    if args.an:
        for alt_name in get_alternative_names(hostname, port):
            print(hostname + ":" + str(port), end=' ')
            print(colored('[' + alt_name + ']', 'light_blue', attrs=['bold']))

    # display subject common name
    if args.cn:
        cname = get_common_name(hostname, port)
        print(hostname + ":" + str(port), end=' ')
        print(colored('[' + cname + ']', 'light_blue', attrs=['bold']))

    print(hostname + ":" + str(port) ,end=' ')

    # display subject organization name
    if args.on:
        oname = get_organization_name(hostname, port)
        if oname:
            print(colored('[' + oname + ']', 'yellow', attrs=['bold']), end=' ')
        else:
            print(colored('[]', 'red', attrs=['bold']), end=' ')

    # display used tls version
    if args.tv:
        tls_version = get_tls_version(hostname, port)
        print(colored('[' + tls_version + ']', 'light_blue', attrs=['bold']), end=' ')

    # display used cipher suite
    if args.cipher:
        cipher_used = check_certificate_strength(hostname, port)[0]
        print(colored('[' + cipher_used + ']', 'light_blue', attrs=['bold']), end=' ')

    # display used hash function
    if args.hash:
        hash_used = get_hashes(hostname, port, args.hash)
        print(colored('[' + hash_used + ']', 'light_blue', attrs=['bold']), end=' ')

    # display used jarm fingerprint
    if args.jarm:
        jarm_used = get_jarm_hash(hostname, port)
        print(colored('[' + jarm_used + ']', 'light_blue', attrs=['bold']), end=' ')

    # display certificate serial number
    if args.sn:
        serial_number = get_serial_number(hostname, port)
        print(colored('[' + serial_number + ']', 'light_blue', attrs=['bold']), end=' ')

    # display certificate pinning status
    if args.pin:
        if check_certificate_pinning(hostname):
            print(colored('[Passed]', 'green', attrs=['bold']), end=' ')
        else:
            print(colored('[Failed]', 'red', attrs=['bold']), end=' ')

    # display certificate authority verification status
    if args.av:
        issued_to, issued_by = check_authority_verification(hostname, port)
        print(colored('[' + issued_to + ']', 'light_blue', attrs=['bold']), end=' ')
        print(colored('[' + issued_by + ']', 'light_blue', attrs=['bold']), end=' ')

    # display certificate valid until
    if args.vu:
        if expired_bool:
            print(colored('[' + expired_str + ']', 'light_blue', attrs=['bold']), end=' ')

    # display host with self-signed certificate
    if args.ss:
        if check_certificate_self_signed(hostname, port):
            print(colored('[Self-Signed]', 'red', attrs=['bold']), end=' ')

    # display host with mismatched certificate
    if args.mm:
        if check_certificate_mismatched(hostname, port):
            print(colored('[Mismatched]', 'red', attrs=['bold']), end=' ')
    
    # display certificate revocation status
    if args.re:
        if not check_certificate_revocation(hostname):
            print(colored('[Revoked]', 'red', attrs=['bold']), end=' ')
        else:
            print(colored('[Not Revoked]', 'green', attrs=['bold']), end=' ')

    # display host with untrusted certificate
    if args.un:
        if not check_certificate_trust(hostname):
            print(colored('[Untrusted]', 'yellow', attrs=['bold']), end=' ')

    # TODO: add support for -list flag

    print()

    if args.j:
        json_out(hostname, port)
