import datetime
import hashlib
from time import time

from Block import Block
from Node import Node
from datetime import time

class Blockchain:
    first = None
    difficulty = 2

    def __init__(self):
        self.first = None
        self.difficulty = 2

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

    def addBlock(self,payload,signer, publicKeyFilename, prvKeyFilename):
        if self.first is None:
            timestamp = time()
            previousHash = "0" * 64
            ownHash = self.hashBlock(payload, timestamp, previousHash, 0,0)
            self.first = Node(Block(payload, timestamp, previousHash, ownHash, 0,signer, publicKeyFilename, prvKeyFilename))

            self.mine(self.difficulty, 0)
            self.first.data.sign()
        else:
            prevNode = self.first
            while prevNode.next != None:
                prevNode = prevNode.next

            timestamp = time()
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

    def isValid(self):
        currNode = self.first
        prevBlockHash = "0" * 64
        while currNode != None:
            if currNode.data.ownHash != self.hashBlock(currNode.data.payload,
                                                       currNode.data.timestamp,
                                                       currNode.data.previousHash,
                                                       currNode.data.index,
                                                       currNode.data.nonce):
                return False

            if currNode.data.previousHash != prevBlockHash:
                return False

            if not currNode.data.verify_signature():
                return False

            prevBlockHash = currNode.data.ownHash
            currNode = currNode.next
        return True

    def sabotage(self,index,payload):
        currNode = self.findNode(index)
        currNode.data.payload = payload
        currNode.data.ownHash = self.hashBlock(currNode.data.payload, currNode.data.timestamp,currNode.data.previousHash,
                                               currNode.data.index,0)

    def printBlockchain(self):
        currNode = self.first
        while currNode != None:
            currNode.data.printBlock()
            currNode = currNode.next

    def findNode(self, index):
        currNode = self.first
        for i in range(index):
            currNode = currNode.next

        return currNode

    def mine(self, difficulty, index):
        starttime = datetime.datetime.now()
        nonce = 0
        currNode = self.findNode(index)
        while not currNode.data.ownHash.startswith("0" * difficulty):
            currNode.data.ownHash = self.hashBlock(currNode.data.payload, currNode.data.timestamp,
                                                             currNode.data.previousHash, currNode.data.index,
                                                             nonce)
            nonce = nonce + 1
        currNode.data.nonce = nonce -1
        endtime = datetime.datetime.now()
        return endtime - starttime



