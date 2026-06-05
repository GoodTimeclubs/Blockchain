class Block:
    index = None
    payload = None
    timestamp = None
    previousHash = None
    ownHash = None
    nonce = 0
    def __init__(self, payload, timestamp, previousHash, ownHash, index, nonce = 0):
        self.payload = payload
        self.timestamp = timestamp
        self.previousHash = previousHash
        self.ownHash = ownHash
        self.index = index
        self.nonce = nonce

    def printBlock(self):
        print("Printing Block with Index:" + str(self.index))
        print("Nonce:         " + str(self.nonce))
        print("Payload:       " + str(self.payload))
        print("Timestamp:     " + str(self.timestamp))
        print("Previous Hash: " + str(self.previousHash))
        print("Own Hash:      " + str(self.ownHash))
        print("")



