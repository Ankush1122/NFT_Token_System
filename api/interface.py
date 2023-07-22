import traceback
import logging
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature

from api.BlockChain.Input import Input
from api.BlockChain.Output import Output
from api.BlockChain.Transaction import Transaction
from api.BlockChain.BlockChain import BlockChain
from api.BlockChain.smartContract import smartContract
import time
from datetime import datetime
from .repo import getBlockchain, add_new_blockchain
blockchain = None
logger = logging.getLogger('django')


def loadBlockChain():
    logger.info("Blockchain Loaded Successfully")
    global blockchain
    blockchain = getBlockchain()


def createBlockChain(difficulty, blockSize, trustedPublicKey, coinToken, genesisAmount):
    global blockchain
    blockchain = BlockChain(difficulty, trustedPublicKey,
                            blockSize, coinToken)
    add_new_blockchain(difficulty, trustedPublicKey, blockSize, coinToken)
    genesis_output = Output(0, genesisAmount,
                            coinToken, trustedPublicKey)
    genesis_transaction = Transaction([genesis_output], [], None, time.time())
    blockchain.createGenesisBlock(genesis_transaction)
    return {"Response": "BlockChain Created Successfully"}


def getBalance(publicKey, token):
    global blockchain
    spendable_outputs = blockchain.getSpendableOutputs(publicKey, token)
    balance = 0
    for output in spendable_outputs:
        balance += output.getValue()
    return {"publicKey": publicKey, "Token": token, "Balance": balance}


def makeTransaction(sender, reciever, amount, token, privateKey, smartContract, allowContract):
    global blockchain
    verified_owner = verifySignature(
        sender, "test", signHash(privateKey, "test"))
    if (verified_owner):
        if (sender == reciever):
            return {"Status": False, "Response": "Self Transaction not allowed"}

        balance = getBalance(sender, token)["Balance"]
        if (balance < amount):
            return {"Status": False, "Response": "Insufficient Balance"}
        if (amount <= 0):
            return {"Status": False, "Response": "Invalid Amount for Transaction"}

        if (not allowContract and sender == blockchain.getTrustedPublicKey() and smartContract is not None):
            return {"Status": False, "Response": "Invalid Transaction, set Smart Contract to None"}

        spendableOutputs = blockchain.getSpendableOutputs(sender, token)

        inputs = []
        amt = 0
        for output in spendableOutputs:
            amt += output.getValue()
            [blockNumber, transactionHash] = blockchain.getOutputPosition(
                output)

            input = Input(blockNumber, transactionHash, output.getIndex(
            ), signHash(privateKey, output.getHash()).hex())
            inputs.append(input)
            if (amt >= amount):
                break

        output1 = Output(0, amount, token, reciever)
        outputs = [output1]
        amt -= amount
        if (amt > 0):
            output2 = Output(1, amt, token, sender)
            outputs.append(output2)

        tx = Transaction(outputs, inputs, smartContract, time.time())

        verified = blockchain.addTransaction(tx)
        if (verified[0]):
            return {"Status": True, "Response": verified[1]}
        else:
            return {"Status": False, "Response": verified[1]}
    else:
        return {"Status": False, "Response": "Invalid Private Key"}


def issueTransaction(owner, amount, token, privateKey):
    global blockchain
    if (owner != blockchain.getTrustedPublicKey()):
        return {"Status": False, "Response": "Only trusted account can make issue transactions"}
    verified_owner = verifySignature(
        owner, "test", signHash(privateKey, "test"))
    if (verified_owner):
        nft_allowed = blockchain.isTokenAllowed(token)
        if (nft_allowed == "not_allowed"):
            return {"Status": False, "Response": "Token not unique"}
        elif (nft_allowed == "allowed" and amount != 1):
            return {"Status": False, "Response": "Only 1 nft must be issued per transaction"}
        else:
            inputs = []
            outputs = [Output(0, amount, token, owner)]
            tx = Transaction(outputs, inputs, None, time.time())
            verified = blockchain.addTransaction(tx)
            if (verified[0]):
                return {"Status": True, "Response": verified[1]}
            else:
                return {"Status": False, "Response": verified[1]}
    else:
        return {"Status": False, "Response": "Invalid Owner Private Key"}


def printBlockChain():
    global blockchain
    blockchain.printBlockChain()


def generateEncryptionKeysPair():
    # Key Generation
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=4096,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return {"publicKey": pem_public, "privateKey": pem_private}


def signHash(privateKey, hash):
    private_key_after = serialization.load_pem_private_key(
        data=privateKey.encode('utf-8'),
        password=None,
        backend=default_backend()
    )
    res = bytes(hash, 'utf-8')
    signature = private_key_after.sign(
        res,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return signature


def verifySignature(publicKey, hash, signature):
    public_key_after = serialization.load_pem_public_key(
        data=publicKey.encode('utf-8'),
        backend=default_backend()
    )
    res = bytes(hash, 'utf-8')
    try:
        public_key_after.verify(
            signature,
            res,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

    except InvalidSignature:
        return False
    else:
        return True


def expireContract(contract, trustedPrivateKey):
    global blockchain
    dic = blockchain.contractStatus(contract)
    if (dic["status"] != "Unexecuted"):
        return {"Status": False, "Response": "Contract have already been executed, Check contract status"}

    if (dic["conditions"] == "Unsatisfied"):
        makeTransaction(blockchain.getTrustedPublicKey(
        ), contract.getSellerPublicKey(), dic["paidSellingAmount"], contract.getSellingToken(), trustedPrivateKey, contract, True)
        makeTransaction(blockchain.getTrustedPublicKey(
        ), contract.getBuyerPublicKey(), dic["paidBuyingAmount"], contract.getBuyingToken(), trustedPrivateKey, contract, True)
        return {"Status": True, "Response": "Contract Expired Successfully"}


def executeContract(contract, trustedPrivateKey):
    global blockchain
    dic = blockchain.contractStatus(contract)
    if (dic["status"] != "Unexecuted"):
        return {"Status": False, "Response": "Contract have already been executed, Check contract status"}

    if (dic["conditions"] == "Satisfied"):
        logger.info(makeTransaction(blockchain.getTrustedPublicKey(
        ), contract.getSellerPublicKey(), dic["paidBuyingAmount"], contract.getBuyingToken(), trustedPrivateKey, contract, True))
        logger.info(makeTransaction(blockchain.getTrustedPublicKey(
        ), contract.getBuyerPublicKey(), dic["paidSellingAmount"], contract.getSellingToken(), trustedPrivateKey, contract, True))
        return {"Status": True, "Response": "Contract Executed Successfully"}
    else:
        return {"Status": False, "Response": "Contract conditions not satisfied yet, Contract can't be executed"}


def getContractStatus(contract):
    global blockchain
    return blockchain.contractStatus(contract)


def getSmartContract(contract):
    date = datetime.strptime(contract.expiryDate, '%d-%m-%Y').date()
    return smartContract(contract.id, contract.sellerPublicKey.replace('\\n', '\n').replace('\\t', '\t').encode('utf-8'), contract.sellingAmount, contract.sellingToken, contract.buyerPublicKey.replace('\\n', '\n').replace('\\t', '\t').encode('utf-8'), contract.buyingAmount, contract.buyingToken, date, contract.physicalAsset)


def readableSmartContract(contract):
    if (contract is None):
        return "None"
    return {"id": contract.getId(), "sellerPublicKey": contract.getSellerPublicKey(), "sellingAmount": contract.getSellingAmount(), "sellingToken": contract.getSellingToken(), "buyerPublicKey": contract.getBuyerPublicKey(), "buyingAmount": contract.getBuyingAmount(), "buyingToken": contract.getBuyingToken(), "expiryDate": contract.getBuyingToken(), "physicalAsset": contract.getPhysicalAsset()}


def getAllTransactions():
    global blockchain
    transactions = blockchain.getAllTransactions()
    response = {}
    for i in range(len(transactions)):
        response["Transaction " +
                 str(i+1)] = readableTransaction(transactions[i])
    return response


def readableTransaction(transaction):
    global blockchain
    inputs = transaction.getInputs()
    if (len(inputs) == 0):
        sender = ""
    else:
        sender = blockchain.getReferencedOutput(inputs[0])[1].getPublicKey()
    reciever = ""
    token = transaction.getOutputs()[0].getToken()
    outputs = transaction.getOutputs()
    for output in outputs:
        if (output.getPublicKey() != sender):
            reciever = output.getPublicKey()
    Amount = 0
    for output in outputs:
        if (output.getPublicKey() != sender):
            Amount += output.getValue()
    contract_id = "None"
    contract = transaction.getSmartContract()
    if (contract):
        contract_id = contract.getId()

    new_inputs = {}
    i = 0
    for input in inputs:
        new_inputs["Input " + str(i)] = {"Block Number": input.getBlockNumber(
        ), "Transaction Hash": input.getTransactionHash(), "Output Index": input.getOutputIndex()}
        i += 1

    new_outputs = {}
    i = 0
    for output in outputs:
        new_outputs["Output " + str(i)] = {"Index": output.getIndex(), "Value": output.getValue(
        ), "Token": output.getToken(), "Public Key": output.getPublicKey()}
        i += 1

    return {"Sender": str(sender), "Reciever": str(reciever), "Amount": Amount, "Token": str(token), "Inputs": new_inputs, "Outputs": new_outputs, "Time Stamp": datetime.fromtimestamp(float(transaction.getTimeStamp())).strftime("%m/%d/%Y, %H:%M:%S"), "transactionHash": transaction.getTransactionHash(), "smartContract": contract_id}


def getNFTHistory(nft):
    global blockchain
    if (nft == blockchain.getCoinToken()):
        return {"Status": False, "Response": "Coin Tokens can not be tracked"}
    transactions = blockchain.getAllTransactions()

    response = {}
    i = 0
    for transaction in transactions:
        tx = readableTransaction(transaction)
        if (tx["Token"] == nft):
            response["Transaction"+str(i+1)] = tx
            i += 1
    return {"Status": True, "Response": response}


def getBlockChain():
    global blockchain
    chain = blockchain.getBlockChain()
    response = {}
    for key in chain:
        if (key != "Transaction Pool" and key != "Chain"):
            response[key] = chain[key]
    d = {}

    for i in range(len(chain["Chain"])):
        d["Block "+str(i)] = {"Index": chain["Chain"][i].getIndex(), "Merkle Root Hash": chain["Chain"][i].getMerkleRoot(), "Self Hash": chain["Chain"]
                              [i].calculateHash(), "Previous Hash": chain["Chain"][i].getPreviousHash(), "Difficulty": chain["Chain"][i].getDifficulty(), "Nonce": chain["Chain"][i].getNonce()}
        d["Block "+str(i)]["Transactions"] = {}
        for j in range(len(chain["Chain"][i].getTransactions())):
            d["Block "+str(i)]["Transactions"]["Transaction"+str(j+1)
                                               ] = readableTransaction(chain["Chain"][i].getTransactions()[j])

    response["Blocks"] = d
    response["Transactions Pool"] = {}
    for j in range(len(chain["Transaction Pool"])):
        response["Transactions Pool"]["Transaction" +
                                      str(j+1)] = readableTransaction(chain["Transaction Pool"][j])

    [chain_connected, valid_proof_of_work,
        valid_transaction_hashes, valid_block_chain] = blockchain.validateBlockChain()
    response["Valid Transaction Hashes"] = valid_transaction_hashes
    response["Valid Block Hashes"] = chain_connected
    response["Valid Proof of Work"] = valid_proof_of_work
    response["Valid Blockchain"] = valid_block_chain

    return response
