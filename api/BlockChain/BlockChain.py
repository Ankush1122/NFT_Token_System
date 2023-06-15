from .Block import Block
from .merkleTree import merkleTree


class BlockChain:
    __chain = None
    __difficulty = None
    __trustedPublicKey = None
    __transactionPool = None
    __blockSize = None
    __coinToken = None

    def __init__(self, difficulty, trustedPublicKey, blockSize, coinToken) -> None:
        self.__chain = []
        self.__difficulty = difficulty
        self.__trustedPublicKey = trustedPublicKey
        self.__transactionPool = []
        self.__blockSize = blockSize
        self.__coinToken = coinToken

    def addTransaction(self, transaction) -> None:
        verified = self.validateTransaction(transaction)
        if (verified[0]):
            self.__transactionPool.append(transaction)
            if (len(self.__transactionPool) >= self.__blockSize):
                self.mineBlock(self.__transactionPool)
                self.__transactionPool = []
        return verified

    def createGenesisBlock(self, genesis_Transaction) -> None:
        verified = self.validateTransaction(genesis_Transaction)
        print(verified[1])
        if (verified[0]):
            self.mineBlock([genesis_Transaction])

    def mineBlock(self, transactions) -> None:
        index = len(self.__chain)
        if index == 0:  # Genesis Block
            previousHash = None
        else:
            previousHash = self.__chain[index - 1].calculateHash()
        tree = merkleTree()
        merkleRoot = tree.create(transactions)
        block = Block(index, transactions, merkleRoot,
                      previousHash, self.__difficulty, 0)
        block.proofOfWork()
        if (block.validateNonce()):
            self.__chain.append(block)

    def validateBlockChain(self) -> bool:
        # Chain is Connected
        size = len(self.__chain)
        for i in range(1, size):
            if (self.__chain[i].getPreviousHash() != self.__chain[i-1].calculateHash()):
                return False

        # Valid Proof Of Work
        for block in self.__chain:
            if (not block.validateNonce()):
                return False

        return True

    def getSpendableOutputs(self, publicKey, token):
        spendable_outputs = []
        transactions = self.getAllTransactions()

        for transaction in transactions:
            for output in transaction.getOutputs():
                if (output.getPublicKey() == publicKey and output.getToken() == token):
                    spendable_outputs.append(output)

        # Removing spent outputs
        for Block in self.__chain:
            for transaction in Block.getTransactions():
                for input in transaction.getInputs():
                    refOutput = self.getReferencedOutput(input)
                    if (refOutput[1] in spendable_outputs):
                        spendable_outputs.remove(refOutput[1])

        # We also remove outputs used in transactions from transaction pool
        for transaction in self.__transactionPool:
            for input in transaction.getInputs():
                refOutput = self.getReferencedOutput(input)
                if (refOutput[1] in spendable_outputs):
                    spendable_outputs.remove(refOutput[1])

        return spendable_outputs

    def validateTransaction(self, transaction) -> bool:
        inputs = transaction.getInputs()
        outputs = transaction.getOutputs()

        outputAmount = 0
        inputAmount = 0

        # "Issue Tokens/Coins" code
        if (len(inputs) == 0 and len(outputs) == 1 and outputs[0].getPublicKey() == self.__trustedPublicKey):
            return [True, "Tokens/Coins Issued Successfully"]

        if (len(inputs) == 0):
            return [False, "No Inputs Included"]

        if (len(outputs) == 0):
            return [False, "No Outputs Included"]

        refOutputs = []
        for input in inputs:
            outputStatus = self.getReferencedOutput(input)
            if (outputStatus[0]):
                refOutputs.append(outputStatus[1])
                if (not outputStatus[1].verifySignature(input.getSignature())):
                    return [False, "Invalid Signature"]
            else:
                return [False, "Invalid Inputs"]

        sender = refOutputs[0].getPublicKey()
        token = refOutputs[0].getToken()

        for output in refOutputs:
            if (sender != output.getPublicKey()):
                return [False, "Inputs belongs to multiple users"]
            if (token != output.getToken()):
                return [False, "Multiple Token Transaction Not Supported"]
            inputAmount += output.getValue()

        spendableOutputs = self.getSpendableOutputs(sender, token)

        for output in refOutputs:
            if (output not in spendableOutputs):
                return [False, "Referenced Input is not Spendable"]

        for output in outputs:
            if (token != output.getToken()):
                return [False, "Multiple Token Transaction Not Supported"]
            outputAmount += output.getValue()

        if (inputAmount != outputAmount):
            return [False, "Unbalanced Transaction Input-Outputs"]

        # Smart Contract Verification code
        smartContract = transaction.getSmartContract()
        if (smartContract is not None):
            status = self.contractStatus(transaction.getSmartContract())
            if (status["status"] == "Expired"):
                return [False, "Contract is Expired, transaction not allowed"]

            if (status["status"] == "Completed"):
                return [False, "Contract is Completed, transaction not allowed"]

            reciever = ""
            singleReciever = True
            for output in outputs:
                if (output.getPublicKey() != sender):
                    if (not singleReciever and reciever != output.getPublicKey()):
                        return [False, "Smart Contract Transaction does not support multiple user output transaction"]
                    if (reciever != output.getPublicKey()):
                        reciever = output.getPublicKey()
                        singleReciever = False

            if (sender == self.__trustedPublicKey):
                return [True, "Transaction Verified"]

            buyer = False
            if (smartContract.getBuyerPublicKey() == sender):
                buyer = True
            elif (smartContract.getSellerPublicKey() == sender):
                buyer = False
            else:
                return [False, "You are not part of Smart Contract"]

            if (reciever != self.__trustedPublicKey):
                return [False, "Smart Contract transaction must be to our Trust Account"]

            if (buyer and token != smartContract.getBuyingToken()):
                return [False, "Invalid buying token according to the smart contract"]

            if (not buyer and token != smartContract.getSellingToken()):
                return [False, "Invalid selling token according to the smart contract"]

        return [True, "Transaction Verified"]

    def getReferencedOutput(self, input):
        if (input.getBlockNumber() > len(self.__chain)):
            return [False, "Invalid Input"]

        transactions = None
        if (input.getBlockNumber() == len(self.__chain)):
            transactions = self.__transactionPool
        else:
            block = self.__chain[input.getBlockNumber()]
            transactions = block.getTransactions()

        transaction = None
        for tx in transactions:
            if (tx.getTransactionHash() == input.getTransactionHash()):
                transaction = tx
                break
        if (transaction is None):
            return [False, "Invalid Input"]

        outputs = transaction.getOutputs()
        for output in outputs:
            if (output.getIndex() == input.getOutputIndex()):
                return [True, output]

    def getOutputPosition(self, output):
        blockIndex = -1
        transactionHash = ""
        for blockNumber in range(len(self.__chain)):
            for transaction in self.__chain[blockNumber].getTransactions():
                for out in transaction.getOutputs():
                    if (out == output):
                        blockIndex = blockNumber
                        transactionHash = transaction.getTransactionHash()
                        break

        for transaction in self.__transactionPool:
            for out in transaction.getOutputs():
                if (out == output):
                    blockIndex = len(self.__chain)
                    transactionHash = transaction.getTransactionHash()
                    break

        return [blockIndex, transactionHash]

    def getBlockChain(self):
        blockchain = {"Difficulty":self.__difficulty, "Trusted Public Key":self.__trustedPublicKey, "Block Size":self.__blockSize, "Coin Token":self.__coinToken, "Transaction Pool":self.__transactionPool, "Chain":self.__chain}
        return blockchain

    def printBlockChain(self) -> None:
        print()
        for block in self.__chain:
            print("Block Index : ", block.getIndex())
            print("Nonce : ", block.getNonce())
            print("Is Nonce Valid : ", block.validateNonce())
            print("Self Hash : ", block.calculateHash())
            print("Previous Hash : ", block.getPreviousHash())
            print("Number of Transactions : ", len(block.getTransactions()))
            print()

        print()
        print("Is Blockchain Valid : ", self.validateBlockChain())
        print("Number of Transactions in Transaction Pool : ",
              len(self.__transactionPool))

    def isTokenAllowed(self, token):
        if (token == self.__coinToken):
            return "coin"
        transactions = self.getAllTransactions()
        for transaction in transactions:
            for output in transaction.getOutputs():
                if (output.getToken() == token):
                    return "not_allowed"
        return "allowed"

    def contractStatus(self, contract):
        paidBuyingAmount = 0
        paidSellingAmount = 0
        transactions = self.getAllTransactions()

        for transaction in transactions:
            if (transaction.getSmartContract() is not None and transaction.getSmartContract().getId() == contract.getId()):
                transactionSenderPublicKey = self.getReferencedOutput(
                    transaction.getInputs()[0])[1].getPublicKey()
                for output in transaction.getOutputs():
                    if (transactionSenderPublicKey == contract.getBuyerPublicKey() and output.getPublicKey() == self.__trustedPublicKey and output.getToken() == contract.getBuyingToken()):
                        paidBuyingAmount += output.getValue()

                    if (transactionSenderPublicKey == contract.getSellerPublicKey() and output.getPublicKey() == self.__trustedPublicKey and output.getToken() == contract.getSellingToken()):
                        paidSellingAmount += output.getValue()

        conditions = ""
        if (paidSellingAmount >= contract.getSellingAmount() and paidBuyingAmount >= contract.getBuyingAmount()):
            conditions = "Satisfied"
        else:
            conditions = "Unsatisfied"

        # Checking if contract is expired
        status = ""
        forwardedBuyingAmount = 0
        forwardedSellingAmount = 0
        ReversedBuyingAmount = 0
        ReversedSellingAmount = 0
        for transaction in transactions:
            if (transaction.getSmartContract() is not None and transaction.getSmartContract().getId() == contract.getId()):
                transactionSenderPublicKey = self.getReferencedOutput(
                    transaction.getInputs()[0])[1].getPublicKey()
                for output in transaction.getOutputs():
                    if (transactionSenderPublicKey == self.__trustedPublicKey and output.getPublicKey() == contract.getSellerPublicKey() and output.getToken() == contract.getBuyingToken()):
                        forwardedBuyingAmount += output.getValue()
                    if (transactionSenderPublicKey == self.__trustedPublicKey and output.getPublicKey() == contract.getBuyerPublicKey() and output.getToken() == contract.getSellingToken()):
                        forwardedSellingAmount += output.getValue()

                    if (transactionSenderPublicKey == self.__trustedPublicKey and output.getPublicKey() == contract.getSellerPublicKey() and output.getToken() == contract.getSellingToken()):
                        ReversedSellingAmount += output.getValue()
                    if (transactionSenderPublicKey == self.__trustedPublicKey and output.getPublicKey() == contract.getBuyerPublicKey() and output.getToken() == contract.getBuyingToken()):
                        ReversedBuyingAmount += output.getValue()

        if (forwardedSellingAmount == 0 and forwardedBuyingAmount == 0 and ReversedBuyingAmount == 0 and ReversedSellingAmount == 0):
            status = "Unexecuted"
        elif (forwardedSellingAmount == paidSellingAmount and forwardedBuyingAmount == paidBuyingAmount):
            status = "Executed"
        elif (ReversedSellingAmount == paidSellingAmount and ReversedBuyingAmount == paidBuyingAmount):
            status = "Expired"

        return {"conditions": conditions, "status": status, "paidBuyingAmount": paidBuyingAmount, "paidSellingAmount": paidSellingAmount}

    def getAllTransactions(self):
        transactions = []
        for Block in self.__chain:
            for transaction in Block.getTransactions():
                transactions.append(transaction)
        for transaction in self.__transactionPool:
            transactions.append(transaction)
        return transactions

    def getTrustedPublicKey(self):
        return self.__trustedPublicKey

    def getCoinToken(self):
        return self.__coinToken