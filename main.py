from BlockChain.BlockChain import BlockChain
from BlockChain.Input import Input
from BlockChain.Output import Output
from BlockChain.Transaction import Transaction
from interface import signHash, generateEncryptionKeysPair

[owner_public_key, owner_private_key] = generateEncryptionKeysPair()

difficulty = 3
blockSize = 2
chain = BlockChain(difficulty, owner_public_key, blockSize)
genesis_output = Output(0, 10000, "coin", owner_public_key)
genesis_transaction = Transaction([genesis_output], [], None)
chain.createGenesisBlock(genesis_transaction)

[user1_public_key, user1_private_key] = generateEncryptionKeysPair()
[user2_public_key, user2_private_key] = generateEncryptionKeysPair()

# Transaction Owner -> User1
input1 = Input(0, genesis_transaction.getTransactionHash(),
               0, signHash(owner_private_key, genesis_output.getHash()))
output1 = Output(0, 2000, "coin", user1_public_key)
output2 = Output(1, 8000, "coin", owner_public_key)

tx1 = Transaction([output1, output2], [input1], None)


# Transaction Owner -> User2
input2 = Input(1, tx1.getTransactionHash(), 1, signHash(
    owner_private_key, output2.getHash()))
output3 = Output(0, 2000, "coin", user2_public_key)
output4 = Output(1, 6000, "coin", owner_public_key)

tx2 = Transaction([output3, output4], [input2], None)

# Transaction User2 -> User1
input3 = Input(1, tx2.getTransactionHash(), 0, signHash(
    user2_private_key, output3.getHash()))
output5 = Output(0, 1000, "coin", user1_public_key)
output6 = Output(1, 1000, "coin", user2_public_key)

tx3 = Transaction([output5, output6], [input3], None)

# Transaction issue owner1
output7 = Output(0, 10000, "coin", owner_public_key)

tx4 = Transaction([output7], [], None)


print(chain.addTransaction(tx1))
print(chain.addTransaction(tx2))
print(chain.addTransaction(tx3))
print(chain.addTransaction(tx4))

chain.printBlockChain()
