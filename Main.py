from Blockchain import Blockchain

bc = Blockchain()
bc.addBlock("hallo")
bc.addBlock("das")
bc.addBlock("ist")
bc.addBlock("ein")
bc.addBlock("test")
#bc.printBlockchain()
#print(bc.isValid())
#bc.sabotage(1,"other")
#bc.printBlockchain()
#print(bc.isValid())





mdif2 = bc.mine(2)
print("Mining duration with difficulty 2: " , mdif2)
bc.first.data.printBlock()

mdif4 = bc.mine(4)
print("Mining duration with difficulty 4: " , mdif4)
bc.first.data.printBlock()

mdif6 = bc.mine(6)
print("Mining duration with difficulty 6: " , mdif6)
bc.first.data.printBlock()