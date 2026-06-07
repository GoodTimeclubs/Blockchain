# Example: build three signed chains with a shared genesis block, then let
# resolve() pick the longest valid one (longest-chain consensus).
from Blockchain import Blockchain
from Authorization import Authorization

# Chain ba: 3 blocks, used as the reference chain calling resolve()
ba = Blockchain()
ba.addBlock("hallo", "Alice", "alice.cert.pem", "alice.key.pem")
ba.addBlock("das", "Alice", "alice.cert.pem", "alice.key.pem")
ba.addBlock("ist", "Alice", "alice.cert.pem", "alice.key.pem")
#ba.addBlock("ist", "Alice", "fake.pem", "fakekey.pem")
#bc.addBlock("ein", "Alice", "alice.cert.pem", "alice.key.pem")
#bc.addBlock("test", "Alice", "alice.cert.pem", "alice.key.pem")
#bc.printBlockchain()
#print(bc.isValid())
#bc.sabotage(1,"other")
#bc.printBlockchain()
#print(bc.isValid())
#print("All blocks are valid and authenticated: ", bc.isValid())

# Chain bb: 5 blocks (the longest candidate)
bb = Blockchain()

bb.addBlock("hallo", "Alice", "alice.cert.pem", "alice.key.pem")
bb.addBlock("das", "Alice", "alice.cert.pem", "alice.key.pem")
bb.addBlock("ist", "Alice", "alice.cert.pem", "alice.key.pem")
bb.addBlock("ein", "Alice", "alice.cert.pem", "alice.key.pem")
bb.addBlock("test", "Alice", "alice.cert.pem", "alice.key.pem")

# Chain bc: 4 blocks (the shorter candidate)
bc = Blockchain()

bc.addBlock("hallo", "Alice", "alice.cert.pem", "alice.key.pem")
bc.addBlock("das", "Alice", "alice.cert.pem", "alice.key.pem")
bc.addBlock("ist", "Alice", "alice.cert.pem", "alice.key.pem")
bc.addBlock("fertig", "Alice", "alice.cert.pem", "alice.key.pem")

# Resolve to the longest valid chain (expected: bb) and print it.
longest = ba.resolve(bb,bc)

longest.printBlockchain()





