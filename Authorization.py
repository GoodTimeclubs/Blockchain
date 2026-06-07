import getpass
import sys

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography import x509
class Authorization:
    certFolderPath = None
    caCertName = None

    def __init__(self, certFolderPath = "./certs/", caCertName = "cacert.pem"):
        self.certFolderPath = certFolderPath
        self.caCertName = caCertName


    def sign(self,payload, prvKeyFilename):
        if isinstance(payload, str):
            payload = payload.encode()  # str -> bytes (UTF-8)
        with open(self.certFolderPath + prvKeyFilename, "rb") as f:
            try:
                private_key = serialization.load_pem_private_key(
                    f.read(),
                    password= (getpass.getpass(prompt='Password for signing key: ')).encode(),
                )

            except ValueError as e:
                print(e)
                sys.exit()


        signature = private_key.sign(
            payload,
            padding.PKCS1v15(),
            hashes.SHA256(),
        )
        return signature

    def verify_signature(self,publicKeyFilename,payload,signature):
        if isinstance(payload, str):
            payload = payload.encode()  # str -> bytes (UTF-8)
        with open(self.certFolderPath + publicKeyFilename, "rb") as f:
            cert = x509.load_pem_x509_certificate(f.read())

        public_key = cert.public_key()

        # RSA:
        try:
            public_key.verify(
                signature,
                payload,
                padding.PKCS1v15(),
                hashes.SHA256(),
            )
            return True

        except InvalidSignature:
            return False



