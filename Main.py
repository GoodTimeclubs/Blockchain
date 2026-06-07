from Blockchain import Blockchain
from Authorization import Authorization

bc = Blockchain()
bc.addBlock("hallo", "Alice", "alicecert.pem", "alicekey.pem")
bc.addBlock("das", "Alice", "alicecert.pem", "alicekey.pem")
bc.addBlock("ist", "Alice", "alicecert.pem", "alicekey.pem")
bc.addBlock("ein", "Alice", "alicecert.pem", "alicekey.pem")
bc.addBlock("test", "Alice", "alicecert.pem", "alicekey.pem")
#bc.printBlockchain()
#print(bc.isValid())
#bc.sabotage(1,"other")
#bc.printBlockchain()
#print(bc.isValid())

print("All blocks are valid and authenticated: ", bc.isValid())




