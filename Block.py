from Authorization import Authorization
class Block:
    index = None
    payload = None
    timestamp = None
    previousHash = None
    ownHash = None
    signer = None
    signature = None
    publicKeyFilename = None
    prvKeyFilename = None
    nonce = 0
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

    def sign(self):
        auth = Authorization()
        self.signature = auth.sign(self.payload, self.prvKeyFilename)


    def verify_signature(self):
        auth = Authorization()
        return auth.verify_signature(self.publicKeyFilename, self.payload, self.signature)

