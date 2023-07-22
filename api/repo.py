from . import models
from operator import attrgetter
from .BlockChain import Input, Output, Transaction, Block, BlockChain


def addTransactionToDB(transaction):
    tx = models.Transaction(index=None, transactionHash=transaction.getTransactionHash(), smartContract=transaction.getSmartContract(
    ), timeStamp=transaction.getTimeStamp(), parentBlock=None)
    tx.save()
    i = 0
    for input in transaction.getInputs():
        inp = models.Input(index=i, blockNumber=input.getBlockNumber(), TransactionHash=input.getTransactionHash(
        ), outputIndex=input.getOutputIndex(), signature=input.getSignature(), parentTransaction=tx)
        inp.save()

    for output in transaction.getOutputs():
        out = models.Output(index=output.getIndex(), value=output.getValue(
        ), token=output.getToken(), publicKey=output.getPublicKey(), parentTransaction=tx)
        out.save()


def addBlockToDB(block):
    blo = models.Block(index=block.getIndex(), merkleRoot=block.getMerkleRoot(
    ), previousHash=block.getPreviousHash(), difficulty=block.getDifficulty(), nonce=block.getNonce())
    blo.save()

    i = 0
    for transaction in block.getTransactions():
        tx = models.Transaction.objects.get(
            transactionHash=transaction.getTransactionHash())
        tx.parentBlock = blo
        tx.index = i
        tx.save()
        i += 1


def getBlockchain():
    info = models.BlockChain.objects.all()
    if (len(info) == 0):
        return None
    else:
        info = info[0]
    inputs_outputs_mapping = {}
    transaction_mapping = {}
    db_inputs = models.Input.objects.all()
    db_outputs = models.Output.objects.all()
    db_transactions = models.Transaction.objects.all()
    db_blocks = models.Block.objects.all()
    transaction_pool = []

    for transaction in db_transactions:
        inputs_outputs_mapping[transaction.transactionHash] = {
            "Inputs": [], "Outputs": []}

    for input in db_inputs:
        inputs_outputs_mapping[input.parentTransaction.transactionHash]["Inputs"].append(
            input)

    for output in db_outputs:
        inputs_outputs_mapping[output.parentTransaction.transactionHash]["Outputs"].append(
            output)

    for block in db_blocks:
        transaction_mapping[block.index] = []

    for transaction in db_transactions:
        inputs_outputs_mapping[transaction.transactionHash]["Inputs"].sort(
            key=attrgetter('index'))
        inputs_outputs_mapping[transaction.transactionHash]["Outputs"].sort(
            key=attrgetter('index'))

        tx_outputs = []
        tx_inputs = []

        for input in inputs_outputs_mapping[transaction.transactionHash]["Inputs"]:
            inp = Input.Input(input.blockNumber, input.TransactionHash,
                              input.outputIndex, input.signature)
            tx_inputs.append(inp)

        for output in inputs_outputs_mapping[transaction.transactionHash]["Outputs"]:
            out = Output.Output(output.index, output.value,
                                output.token, output.publicKey)
            tx_outputs.append(out)

        tx = Transaction.Transaction(tx_outputs, tx_inputs,
                                     transaction.smartContract, transaction.timeStamp)
        if (transaction.parentBlock is not None):
            transaction_mapping[transaction.parentBlock.index].append(
                (transaction.index, tx))
        else:
            transaction_pool.append(tx)

    blocks = []
    for block in db_blocks:
        transaction_mapping[block.index].sort()
        txs = []
        for index, tx in transaction_mapping[block.index]:
            txs.append(tx)
        blo = Block.Block(block.index, txs, block.merkleRoot,
                          block.previousHash, block.difficulty, block.nonce)
        blocks.append(blo)
    blocks.sort(key=lambda x: x.getIndex())
    blockchain = BlockChain.BlockChain(
        info.difficulty, info.trustedPublicKey, info.blockSize, info.coinToken, blocks, transaction_pool)
    return blockchain


def add_new_blockchain(difficulty, trustedPublicKey, blockSize, coinToken):
    models.Input.objects.all().delete()
    models.Output.objects.all().delete()
    models.Transaction.objects.all().delete()
    models.Block.objects.all().delete()
    models.BlockChain.objects.all().delete()
    blockchain = models.BlockChain(
        difficulty=difficulty, trustedPublicKey=trustedPublicKey, blockSize=blockSize, coinToken=coinToken)
    blockchain.save()
