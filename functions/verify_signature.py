from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from base64 import b64decode
class PyCrypto:

    def verify_sign(pub_key, signature, data):
        '''
        Verifies with a public key from whom the data came that it was indeed
        signed by their private key
        param: public_key_loc Path to public key
        param: signature String signature to be verified
        return: Boolean. True if the signature is valid; False otherwise.
        '''
        rsakey = RSA.importKey(bytes(pub_key,'ascii'))
        signer = PKCS1_v1_5.new(rsakey)
        digest = SHA256.new()
        # Assumes the data is base64 encoded to begin with
        digest.update(b64decode(data))
        print (digest)
        print("\n"+b64decode(signature))
        if signer.verify(digest, b64decode(signature)):
            return True
        return False
