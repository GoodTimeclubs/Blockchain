from Authorization import Authorization

# A single block in the chain: holds the payload, its hashes, and the author's signature.
class Block:
    index = None              # position of the block in the chain (genesis = 0)
    payload = None            # arbitrary data stored in the block
    timestamp = None          # creation time of the block
    previousHash = None       # hash of the preceding block (64 zeros for genesis)
    ownHash = None            # SHA-256 hash over this block's contents
    signer = None             # human-readable name of the author
    signature = None          # digital signature of the payload (set by sign())
    publicKeyFilename = None  # certificate file used to verify the signature
    prvKeyFilename = None     # private key file used to create the signature
    nonce = 0                 # counter varied during proof-of-work mining
    def __init__(self,
                 payload,
                 timestamp,
                 previousHash,
                 ownHash,
                 index,
                 signer,
                 publicKeyFilename,
                 prvKeyFilename,
                 nonce = 0):
        self.payload = payload
        self.timestamp = timestamp
        self.previousHash = previousHash
        self.ownHash = ownHash
        self.index = index
        self.signer = signer
        self.publicKeyFilename = publicKeyFilename
        self.prvKeyFilename = prvKeyFilename
        self.nonce = nonce

    # Pretty-print all fields of this block to stdout.
    def printBlock(self):
        print("Printing Block with Index:" + str(self.index))
        print("Nonce:         " + str(self.nonce))
        print("Payload:       " + str(self.payload))
        print("Timestamp:     " + str(self.timestamp))
        print("Previous Hash: " + str(self.previousHash))
        print("Own Hash:      " + str(self.ownHash))
        print("Signer:        " + str(self.signer))
        print("Public Key:    " + str(self.publicKeyFilename))
        print("Private Key:   " + str(self.prvKeyFilename))
        print("")

    # Sign the payload with the author's private key and store the signature.
    def sign(self):
        auth = Authorization()
        self.signature = auth.sign(self.payload, self.prvKeyFilename)


    # Check the author's signature/certificate via the Authorization helper.
    def verify_signature(self):
        auth = Authorization()
        return auth.verify_signature(self.publicKeyFilename, self.payload, self.signature)

