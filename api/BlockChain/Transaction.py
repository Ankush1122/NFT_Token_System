import hashlib


class Transaction:
    __inputs = None
    __outputs = None
    __transactionHash = None
    __smartContract = None
    __timeStamp = None

    def __init__(self, outputs, inputs, smartContract, timeStamp) -> None:
        self.__inputs = inputs
        self.__outputs = outputs
        self.__smartContract = smartContract
        self.__transactionHash = self.calculateHash()
        self.__timeStamp = timeStamp

    def calculateHash(self):
        hash = ""
        for output in self.__outputs:
            hash = hashlib.sha256(
                (hash + output.getHash()).encode('utf-8')).hexdigest()
        for input in self.__inputs:
            hash = hashlib.sha256(
                (hash + input.getHash()).encode('utf-8')).hexdigest()
        if self.__smartContract is not None:
            hash += self.__smartContract.getHash()
        hash += str(self.__timeStamp)
        return hashlib.sha256(hash.encode('utf-8')).hexdigest()

    def getInputs(self):
        return self.__inputs

    def getOutputs(self):
        return self.__outputs

    def getTransactionHash(self):
        return self.__transactionHash

    def getSmartContract(self):
        return self.__smartContract

    def getTimeStamp(self):
        return self.__timeStamp
