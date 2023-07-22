import hashlib


class Input:
    __blockNumber = None
    __transactionHash = None
    __outputIndex = None
    __signature = None

    def __init__(self, blockNumber, transactionHash, outputIndex, signature) -> None:
        self.__blockNumber = blockNumber
        self.__transactionHash = transactionHash
        self.__outputIndex = outputIndex
        self.__signature = signature

    def getHash(self) -> str:
        return hashlib.sha256(str(self).encode('utf-8')).hexdigest()

    def __str__(self) -> str:
        return str(self.__blockNumber) + str(self.__transactionHash) + str(self.__outputIndex) + str(self.__signature)

    def getBlockNumber(self):
        return self.__blockNumber

    def getTransactionHash(self):
        return self.__transactionHash

    def getOutputIndex(self):
        return self.__outputIndex

    def getSignature(self):
        return self.__signature
