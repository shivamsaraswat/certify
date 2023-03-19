import subprocess


def check_certificate_trust(hostname) -> bool:
    """
    Checks if a certificate is trusted

    :param hostname: The hostname to check
    :type hostname: str

    :return: True if the certificate is trusted, False otherwise
    :rtype: bool
    """

    stop = False
    trust = True

    try:

        # Run the openssl s_client command and capture the output
        with subprocess.Popen(["openssl", "s_client", "-connect", f"{hostname}:443"], stdout=subprocess.PIPE, stderr=subprocess.STDOUT) as proc:

            while True:
                line = proc.stdout.readline()
                if not line:
                    break
                if "Verify return code:" in line.decode().strip():
                    if "certificate not trusted" in line.decode():
                        trust = False
                    stop = True
                    break

            if stop:
                proc.kill()

    except Exception:
        pass

    return trust
