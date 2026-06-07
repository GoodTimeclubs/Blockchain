import datetime
import hashlib
from time import time

from Block import Block
from Node import Node
from datetime import time

# A blockchain stored as a singly linked list of Nodes, each holding one Block.
class Blockchain:
    first = None      # head Node of the chain (genesis block)
    difficulty = 2    # number of leading zeros a valid hash must have (PoW)

    def __init__(self):
        self.first = None
        self.difficulty = 2

    # Compute the SHA-256 hash over all hash-relevant fields of a block.
    def hashBlock(self,
                  payload,
                  timestamp,
                  previousHash,
                  index,
                  nonce):
        sha = hashlib.sha256()
        sha.update(str(payload).encode())
        sha.update(str(timestamp).encode())
        sha.update(previousHash.encode())
        sha.update(str(index).encode())
        sha.update(str(nonce).encode())
        return sha.hexdigest()

    # Append a new block to the end of the chain, then mine and sign it.
    def addBlock(self,payload,signer, publicKeyFilename, prvKeyFilename):
        timestamp = datetime.datetime.now()
        if self.first is None:
            # genesis block: no predecessor, so previous hash is 64 zeros
            previousHash = "0" * 64
            ownHash = self.hashBlock(payload, timestamp, previousHash, 0,0)
            self.first = Node(Block(payload, timestamp, previousHash, ownHash, 0,signer, publicKeyFilename, prvKeyFilename))

            self.mine(self.difficulty, 0)
            self.first.data.sign()
        else:
            # walk to the tail of the list to find the last block
            prevNode = self.first
            while prevNode.next != None:
                prevNode = prevNode.next

            # link the new block to its predecessor and increment the index
            preciousHash = prevNode.data.ownHash
            index = prevNode.data.index +1
            currNode = Node(Block(payload,
                                  timestamp,
                                  preciousHash,
                                  self.hashBlock(payload,
                                                timestamp,
                                                preciousHash,
                                                index,
                                                0),
                                  index,
                                  signer,
                                  publicKeyFilename,
                                  prvKeyFilename,
                                  ))

            prevNode.next = currNode
            self.mine(self.difficulty, index)
            currNode.data.sign()

    # Walk the whole chain and check hashes, links and signatures.
    def isValid(self):
        currNode = self.first
        prevBlockHash = "0" * 64
        while currNode != None:
            # 1) the stored hash must match a fresh recomputation
            if currNode.data.ownHash != self.hashBlock(currNode.data.payload,
                                                       currNode.data.timestamp,
                                                       currNode.data.previousHash,
                                                       currNode.data.index,
                                                       currNode.data.nonce):
                print("Wrong hash in the following Block:")
                currNode.data.printBlock()
                return False

            # 2) the previous-hash link must point to the prior block
            if currNode.data.previousHash != prevBlockHash:
                print("Wrong previous hash in the following Block:")
                currNode.data.printBlock()
                return False

            # 3) the author's signature/certificate must be valid
            if not currNode.data.verify_signature():
                print("Error while verifying the signature in the following Block:")
                currNode.data.printBlock()
                return False

            prevBlockHash = currNode.data.ownHash
            currNode = currNode.next
        return True

    # Tamper with a block's payload (for testing how validation reacts).
    def sabotage(self,index,payload):
        currNode = self.findNode(index)
        currNode.data.payload = payload
        currNode.data.ownHash = self.hashBlock(currNode.data.payload, currNode.data.timestamp,currNode.data.previousHash,
                                               currNode.data.index,0)

    # Print every block in the chain from head to tail.
    def printBlockchain(self):
        currNode = self.first
        while currNode != None:
            currNode.data.printBlock()
            currNode = currNode.next

    # Return the Node at the given position (0-based) by walking the list.
    def findNode(self, index):
        currNode = self.first
        for i in range(index):
            currNode = currNode.next

        return currNode

    # Return the number of blocks in the chain.
    def getLength(self):
        prevNode = self.first
        while prevNode.next != None:
            prevNode = prevNode.next
        return prevNode.data.index +1

    # Proof-of-work: vary the nonce until the block's hash has the
    # required number of leading zeros. Returns the time it took.
    def mine(self, difficulty, index):
        starttime = datetime.datetime.now()
        nonce = 0
        currNode = self.findNode(index)
        # keep rehashing with an increasing nonce until the target is met
        while not currNode.data.ownHash.startswith("0" * difficulty):
            currNode.data.ownHash = self.hashBlock(currNode.data.payload, currNode.data.timestamp,
                                                             currNode.data.previousHash, currNode.data.index,
                                                             nonce)
            nonce = nonce + 1
        currNode.data.nonce = nonce -1
        endtime = datetime.datetime.now()
        return endtime - starttime

    # Longest-chain consensus: pick the longer of two candidate chains,
    # provided it is valid and shares this chain's genesis payload.
    # On equal length, prefer the first valid chain; None if neither is valid.
    def resolve (self, chain_a : Blockchain, chain_b :Blockchain):
        chain_aLength = chain_a.getLength()
        chain_bLength = chain_b.getLength()

        # chain_b is longer -> accept it if valid and same origin
        if(chain_aLength < chain_bLength):
            if chain_b.isValid() and chain_b.first.data.payload == self.first.data.payload:
                return chain_b

        # chain_a is longer -> accept it if valid and same origin
        if (chain_aLength > chain_bLength):
            if chain_a.isValid() and chain_a.first.data.payload == self.first.data.payload:
                return chain_a

        # equal length -> take whichever chain is valid (a wins ties)
        if (chain_aLength == chain_bLength):
            if chain_a.isValid():
                return chain_a

            elif chain_b.isValid():
                return chain_b

            else:
                return None

