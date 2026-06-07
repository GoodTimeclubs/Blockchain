import getpass
import sys

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from cryptography import x509

# Handles author authentication: signing payloads with a private key and
# validating the author's X.509 certificate against a trusted CA certificate.
class Authorization:
    certFolderPath = None  # directory holding keys and certificates
    caCertName = None      # filename of the trusted CA certificate

    def __init__(self, certFolderPath = "./certs/", caCertName = "cacert.pem"):
        self.certFolderPath = certFolderPath
        self.caCertName = caCertName


    # Sign the payload with an RSA private key (PKCS#1 v1.5 + SHA-256).
    def sign(self,payload, prvKeyFilename):
        if isinstance(payload, str):
            payload = payload.encode()  # str -> bytes (UTF-8)



        with open(self.certFolderPath + prvKeyFilename, "rb") as f:

            key_data = f.read()

            try:
                # first try to load the key assuming it is not password-protected
                private_key = serialization.load_pem_private_key(key_data, password=None)

            except TypeError:
                # key is encrypted: prompt the user for the passphrase and retry
                try:
                    private_key = serialization.load_pem_private_key(
                        key_data,
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

    # Verify that the author's certificate was issued by the trusted CA,
    # i.e. that the signer is authenticated. Returns True/False.
    def verify_signature(self,publicKeyFilename,payload,signature):
        if isinstance(payload, str):
            payload = payload.encode()  # str -> bytes (UTF-8)
        # load the author's certificate and the trusted CA certificate
        with open(self.certFolderPath + publicKeyFilename, "rb") as f:
            cert = x509.load_pem_x509_certificate(f.read())

        with open(self.certFolderPath + self.caCertName, "rb") as f:
            ca_cert = x509.load_pem_x509_certificate(f.read())

        ca_public_key = ca_cert.public_key()

        try:
            # check the certificate's signature against the CA's public key
            ca_public_key.verify(
                cert.signature,
                cert.tbs_certificate_bytes,
                padding.PKCS1v15(),
                cert.signature_hash_algorithm,
            )
            return True
        except InvalidSignature:
            return False



