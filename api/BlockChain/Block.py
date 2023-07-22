import hashlib


class Block:

    __index = None
    __transactions = None
    __merkleRoot = None
    __previousHash = None
    __difficulty = None
    __nonce = None

    def __init__(self, index, transactions, merkleRoot, previousHash, difficulty, nonce) -> None:
        self.__index = index
        self.__transactions = transactions
        self.__merkleRoot = merkleRoot
        self.__previousHash = previousHash
        self.__difficulty = difficulty
        self.__nonce = nonce

    def calculateHash(self) -> str:
        return hashlib.sha256(str(self).encode('utf-8')).hexdigest()

    def validateNonce(self) -> bool:
        hash = self.calculateHash()
        for i in range(self.__difficulty):
            if hash[i] != '0':
                return False
        return True

    def getIndex(self):
        return self.__index

    def getTransactions(self):
        return self.__transactions

    def getMerkleRoot(self):
        return self.__merkleRoot

    def getPreviousHash(self):
        return self.__previousHash

    def getDifficulty(self):
        return self.__difficulty

    def getNonce(self):
        return self.__nonce

    def proofOfWork(self) -> None:
        i = 1
        while True:
            foundNonce = True
            self.__nonce = i
            hash = self.calculateHash()
            for j in range(self.__difficulty):
                if hash[j] != '0':
                    foundNonce = False
                    break
            if foundNonce:
                break
            i += 1

    def __str__(self) -> str:
        return str(self.__index) + str(self.__merkleRoot) + str(self.__previousHash) + str(self.__difficulty) + str(self.__nonce)
