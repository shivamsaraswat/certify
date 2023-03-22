import sys
import json as jsonlib
from termcolor import colored
from input_args import parse_arguments

from probes.jarm_hash import get_jarm_hash
from probes.calculate_hash import get_hashes
from probes.tls_version import get_tls_version
from probes.common_name import get_common_name
from probes.serial_number import get_serial_number
from probes.alternative_names import get_alternative_names
from probes.organization_name import get_organization_name
from probes.certificate_pinning import check_certificate_pinning
from probes.certificate_strength import check_certificate_strength
from probes.certificate_authority_verification import check_authority_verification

from misconfigurations.certificate_trust import check_certificate_trust
from misconfigurations.certificate_revocation import check_certificate_revocation
from misconfigurations.certificate_expiration import check_certificate_expiration
from misconfigurations.certificate_mismatched import check_certificate_mismatched
from misconfigurations.certificate_self_signed import check_certificate_self_signed


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

    json_out_dict = dict()

    # store certificate expiration status
    expired_bool, reason_or_valid_until = check_certificate_expiration(hostname, port)
    if expired_bool == False:
        json_out_dict['Expired'] = 'Yes'

    # store subject alternative names
    alt_names = list()
    for alt_name in get_alternative_names(hostname, port):
        alt_names.append(alt_name)
    json_out_dict['Alternative Names'] = alt_names

    # store subject common name
    cname = get_common_name(hostname, port)
    json_out_dict['Common Name'] = cname

    # store subject organization name
    oname = get_organization_name(hostname, port)
    if oname:
        json_out_dict['Organization Name'] = oname
    else:
        json_out_dict['Organization Name'] = None

    # store used tls version
    tls_version, issue = get_tls_version(hostname, port)
    json_out_dict['TLS Version'] = tls_version
    json_out_dict['Issue'] = issue

    # store used cipher suite
    cipher_used, cipher_strength = check_certificate_strength(hostname, port)
    json_out_dict['Cipher Suite'] = cipher_used
    json_out_dict['Cipher Strength'] = cipher_strength

    # store used fingerprint_hash
    hash_used = get_hashes(hostname, port, args.hash, True)
    json_out_dict['Fingerprint Hash'] = hash_used

    # store used jarm fingerprint
    jarm_value = get_jarm_hash(hostname, port)
    json_out_dict['JARM'] = jarm_value

    # store certificate serial number
    serial_number = get_serial_number(hostname, port)
    json_out_dict['Serial Number'] = serial_number

    # store certificate pinning status
    if check_certificate_pinning(hostname):
        json_out_dict['Certificate Pinning'] = 'Passed'
    else:
        json_out_dict['Certificate Pinning'] = 'Failed'

    # store certificate authority verification status
    issued_to, issued_by = check_authority_verification(hostname, port)
    json_out_dict['Certificate Issued To'] = issued_to
    json_out_dict['Certificate Issued By'] = issued_by

    # store certificate valid until
    if expired_bool:
        json_out_dict['Valid Until'] = reason_or_valid_until

    # store host with self-signed certificate
    if check_certificate_self_signed(hostname, port):
        json_out_dict['Self-Signed'] = 'Yes'
    else:
        json_out_dict['Self-Signed'] = 'No'

    # store host with mismatched certificate
    if check_certificate_mismatched(hostname, port):
        json_out_dict['Mismatched'] = 'Yes'
    else:
        json_out_dict['Mismatched'] = 'No'

    # store certificate revocation status
    if not check_certificate_revocation(hostname):
        json_out_dict['Revoked'] = 'Yes'
    else:
        json_out_dict['Revoked'] = 'No'

    # store host with untrusted certificate
    if not check_certificate_trust(hostname):
        json_out_dict['Untrusted'] = 'Yes'
    else:
        json_out_dict['Untrusted'] = 'No'

    print("\n" + hostname)
    print(jsonlib.dumps(json_out_dict, indent=4))

    # Write to the output file
    if output:
        with open(output.name, 'a') as f:
            jsonlib.dump(json_out_dict, f, indent=4)
            f.write('\n')


if __name__ == '__main__':

    args = parse_arguments()
    hostname = args.d
    file_to_read = args.l
    port = args.port
    output = args.output

    # Initialize the variables
    output_str = str()
    hostnames = list()

    if not args.silent:
        logo()

    if not hostname and not file_to_read:
        print(colored('[-] Error: Please specify a domain name or a file containing hostnames.', 'red', attrs=['bold']))
        sys.exit(0)

    if hostname:
        hostnames = list(set(hostname.split(',')))

    # read the list of hostnames from the file
    if file_to_read:
        with open(file_to_read, 'r') as f:
            for domain in f.readlines():
                hostnames.append(domain.strip())

    for hostname in hostnames:

        # handle json output
        if args.j:
            json_out(hostname, port)
            continue

        probes_specified = args.on or args.j or args.tv or args.cipher or args.hash or args.jarm or args.sn or args.pin or args.av or args.ex or args.ss or args.mm or args.re or args.un
        if (args.an or args.cn) and probes_specified:
            print(colored('[-] Error: -an and -cn cannot be used with other probe flags.', 'red', attrs=['bold']))
            sys.exit(0)

        # display subject alternative names
        if args.an:
            for alt_name in get_alternative_names(hostname, port):
                print(hostname + ":" + str(port), end=' ')
                print(colored('[' + alt_name + ']', 'light_blue', attrs=['bold']))
                if output:
                    output_str += hostname + ":" + str(port) + ' [' + alt_name + ']\n'

        # display subject common name
        if args.cn:
            cname = get_common_name(hostname, port)
            print(hostname + ":" + str(port), end=' ')
            print(colored('[' + cname + ']', 'light_blue', attrs=['bold']))
            if output:
                output_str += hostname + ":" + str(port) + ' [' + cname + ']\n'

        if not args.j and not args.an and not args.cn:
            print(hostname + ":" + str(port) ,end=' ')

        if output and not args.an and not args.cn:
            output_str = hostname + ":" + str(port)

        # display certificate expiration status
        expired_bool, reason_or_valid_until = check_certificate_expiration(hostname, port)
        if args.ex:
            if expired_bool == False:
                print(colored('[Expired]', 'red', attrs=['bold']), end=' ')
                if output:
                    output_str += ' [Expired]'

        # display subject organization name
        if args.on:
            oname = get_organization_name(hostname, port)
            if oname:
                print(colored('[' + oname + ']', 'yellow', attrs=['bold']), end=' ')
                if output:
                    output_str += ' [' + oname + ']'

        # display used tls version
        if args.tv:
            tls_version, _ = get_tls_version(hostname, port)
            print(colored('[' + tls_version + ']', 'light_blue', attrs=['bold']), end=' ')
            if output:
                output_str += ' [' + tls_version + ']'

        # display used cipher suite
        if args.cipher:
            cipher_used, cipher_strength = check_certificate_strength(hostname, port)
            print(colored('[' + cipher_used + ']', 'light_blue', attrs=['bold']), end=' ')
            print(colored('[' + cipher_strength + ']', 'light_blue', attrs=['bold']), end=' ')
            if output:
                output_str += ' [' + cipher_used + '] [' + cipher_strength + ']'

        # display used hash function
        if args.hash:
            hash_used = get_hashes(hostname, port, args.hash)
            print(colored('[' + hash_used + ']', 'light_blue', attrs=['bold']), end=' ')
            if output:
                output_str += ' [' + hash_used + ']'

        # display used jarm fingerprint
        if args.jarm:
            jarm_value = get_jarm_hash(hostname, port)
            print(colored('[' + jarm_value + ']', 'light_blue', attrs=['bold']), end=' ')
            if output:
                output_str += ' [' + jarm_value + ']'

        # display certificate serial number
        if args.sn:
            serial_number = get_serial_number(hostname, port)
            print(colored('[' + serial_number + ']', 'light_blue', attrs=['bold']), end=' ')
            if output:
                output_str += ' [' + serial_number + ']'

        # display certificate pinning status
        if args.pin:
            if check_certificate_pinning(hostname):
                print(colored('[Passed]', 'green', attrs=['bold']), end=' ')
                if output:
                    output_str += ' [Passed]'
            else:
                print(colored('[Failed]', 'red', attrs=['bold']), end=' ')
                if output:
                    output_str += ' [Failed]'

        # display certificate authority verification status
        if args.av:
            issued_to, issued_by = check_authority_verification(hostname, port)
            print(colored('[' + issued_to + ']', 'light_blue', attrs=['bold']), end=' ')
            print(colored('[' + issued_by + ']', 'light_blue', attrs=['bold']), end=' ')
            if output:
                output_str += ' [' + issued_to + '] [' + issued_by + ']'

        # display certificate valid until
        if args.vu:
            if expired_bool:
                print(colored('[' + reason_or_valid_until + ']', 'light_blue', attrs=['bold']), end=' ')
                if output:
                    output_str += ' [' + reason_or_valid_until + ']'

        # display host with self-signed certificate
        if args.ss:
            if check_certificate_self_signed(hostname, port):
                print(colored('[Self-Signed]', 'red', attrs=['bold']), end=' ')
                if output:
                    output_str += ' [Self-Signed]'

        # display host with mismatched certificate
        if args.mm:
            if check_certificate_mismatched(hostname, port):
                print(colored('[Mismatched]', 'red', attrs=['bold']), end=' ')
                if output:
                    output_str += ' [Mismatched]'

        # display certificate revocation status
        if args.re:
            if not check_certificate_revocation(hostname):
                print(colored('[Revoked]', 'red', attrs=['bold']), end=' ')
                if output:
                    output_str += ' [Revoked]'
            else:
                print(colored('[Not Revoked]', 'green', attrs=['bold']), end=' ')
                if output:
                    output_str += ' [Not Revoked]'

        # display host with untrusted certificate
        if args.un:
            if not check_certificate_trust(hostname):
                print(colored('[Untrusted]', 'yellow', attrs=['bold']), end=' ')
                if output:
                    output_str += ' [Untrusted]'

        # Write to the output file
        if output:
            with open(output.name, 'a') as f:
                f.write(output_str + '\n')

        print()
