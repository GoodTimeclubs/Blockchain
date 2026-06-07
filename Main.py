from Blockchain import Blockchain
from Authorization import Authorization

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

bb = Blockchain()

bb.addBlock("hallo", "Alice", "alice.cert.pem", "alice.key.pem")
bb.addBlock("das", "Alice", "alice.cert.pem", "alice.key.pem")
bb.addBlock("ist", "Alice", "alice.cert.pem", "alice.key.pem")
bb.addBlock("ein", "Alice", "alice.cert.pem", "alice.key.pem")
bb.addBlock("test", "Alice", "alice.cert.pem", "alice.key.pem")

bc = Blockchain()

bc.addBlock("hallo", "Alice", "alice.cert.pem", "alice.key.pem")
bc.addBlock("das", "Alice", "alice.cert.pem", "alice.key.pem")
bc.addBlock("ist", "Alice", "alice.cert.pem", "alice.key.pem")
bc.addBlock("fertig", "Alice", "alice.cert.pem", "alice.key.pem")

longest = ba.resolve(bb,bc)

longest.printBlockchain()





