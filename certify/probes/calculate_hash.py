import ssl
import socket
import hashlib


def get_hashes(hostname, port, hash_name=None, all_hash=False) -> str or dict:
    """
    Gets the fingerprint hashes of a certificate

    :param hostname: The hostname to check
    :type hostname: str
    :param port: The port to check
    :type port: int
    :param hash_name: The hash to use
    :type hash_name: str
    :param all_hash: Return all hashes
    :type all_hash: bool

    :return: The fingerprint hashes of a certificate
    :rtype: str or dict
    """

    try:
        # Establish SSL connection and get certificate
        with ssl.create_default_context().wrap_socket(socket.socket(), server_hostname=hostname) as ssock:
            ssock.connect((hostname, port))
            cert = ssock.getpeercert(binary_form=True)

        # Return the hash of the certificate
        if hash_name == 'md5':
            return hashlib.md5(cert).hexdigest()
        elif hash_name == 'sha1':
            return hashlib.sha1(cert).hexdigest()
        elif hash_name == 'sha224':
            return hashlib.sha224(cert).hexdigest()
        elif hash_name == 'sha256':
            return hashlib.sha256(cert).hexdigest()
        elif hash_name == 'sha384':
            return hashlib.sha384(cert).hexdigest()
        elif hash_name == 'sha512':
            return hashlib.sha512(cert).hexdigest()
        elif all_hash:
            # calculate all hashes
            all_hashes = dict()
            all_hashes['md5'] = hashlib.md5(cert).hexdigest()
            all_hashes['sha1'] = hashlib.sha1(cert).hexdigest()
            all_hashes['sha224'] = hashlib.sha224(cert).hexdigest()
            all_hashes['sha256'] = hashlib.sha256(cert).hexdigest()
            all_hashes['sha384'] = hashlib.sha384(cert).hexdigest()
            all_hashes['sha512'] = hashlib.sha512(cert).hexdigest()
            return all_hashes

    except Exception:
        pass

    return ""
