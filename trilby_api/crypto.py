from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from struct import pack
import base64
import hashlib

def base64url_encode(data):
    """
    base64-encodes its input, using the modified URL-safe
    alphabet given in RFC 4648.
    """
    b = base64.b64encode(s=data,
            altchars=b'-_')
    return str(b, encoding='ASCII')

def bignum_to_bytes(bignum):

    temp = bignum
    result = []

    while temp!=0:
        result.append(temp & 0xFF)
        temp >>= 8

    result.reverse()
    return bytes(result)

class Key(object):
    """
    An RSA public/private key pair, which can produce
    a magic-envelope signature for itself.

    I was going to subclass the RSA key object,
    but it's hidden away and has an underscore prefix,
    so I guess the developers thought that was a bad idea.
    So I'm wrapping it, instead.
    """

    def __init__(self):
        self._rsa_key = RSA.generate(1024)

    def private_as_pem(self):
        return self._rsa_key.exportKey('PEM')

    def public_as_pem(self):
        return self._rsa_key.publickey().exportKey('PEM')

    def modulus(self):
        return self._rsa_key.n
    
    def public_exponent(self):
        return self._rsa_key.e

    def private_exponent(self):
        return self._rsa_key.d

    def magic_envelope(self):
        return 'RSA.{0}.{1}'.format(
                base64url_encode(
                    bignum_to_bytes(
                        self._rsa_key.n)),
                base64url_encode(
                    bignum_to_bytes(
                        self._rsa_key.e)),
                )
