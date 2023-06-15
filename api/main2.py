from api.interface import *

difficulty = 3
blockSize = 2
coinToken = "coin"
genesisAmount = 10000
d = generateEncryptionKeysPair()
owner_private_key = d["Private Key"]
owner_public_key = d["Public Key"]


createBlockChain(difficulty, blockSize, owner_public_key,
                 coinToken, genesisAmount)

d = generateEncryptionKeysPair()
user1_private_key = d["Private Key"]
user1_public_key = d["Public Key"]

d = generateEncryptionKeysPair()
user2_private_key = d["Private Key"]
user2_public_key = d["Public Key"]

makeTransaction(owner_public_key, user1_public_key,
                2000, coinToken, owner_private_key, None)

makeTransaction(owner_public_key, user2_public_key,
                2000, coinToken, owner_private_key, None)


print("Balance Owner : ", getBalance(owner_public_key, coinToken)["Balance"])
print("Balance User1 : ", getBalance(user1_public_key, coinToken)["Balance"])
print("Balance User2 : ", getBalance(user2_public_key, coinToken)["Balance"])

nft = "nft1"
issueTransaction(owner_public_key, 1, nft, owner_private_key)

makeTransaction(owner_public_key, user1_public_key,
                1, nft, owner_private_key, None)

print("NFT Balance Owner : ", getBalance(owner_public_key, nft)["Balance"])
print("NFT Balance User1 : ", getBalance(user1_public_key, nft)["Balance"])
print("NFT Balance User2 : ", getBalance(user2_public_key, nft)["Balance"])

contract = makeSmartContract(
    "id1", user1_public_key, 1, nft, user2_public_key, 1000, coinToken, "", None)
print(getContractStatus(contract))

makeTransaction(user2_public_key, user1_public_key, 500,
                coinToken, user2_private_key, contract)

makeTransaction(user2_public_key, owner_public_key, 500,
                coinToken, user2_private_key, contract)
print(getContractStatus(contract))

makeTransaction(user2_public_key, owner_public_key, 510,
                coinToken, user2_private_key, contract)
print(getContractStatus(contract))


makeTransaction(user1_public_key, owner_public_key, 1,
                coinToken, user1_private_key, contract)

makeTransaction(user1_public_key, owner_public_key, 1,
                nft, user1_private_key, contract)
print(getContractStatus(contract))

printBlockChain()

executeContract(contract, owner_private_key)