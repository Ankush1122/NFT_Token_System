from django.db import models


class SmartContract(models.Model):
    id = models.TextField(primary_key=True)
    sellerPublicKey = models.TextField()
    sellingAmount = models.BigIntegerField()
    sellingToken = models.TextField()
    buyerPublicKey = models.TextField()
    buyingAmount = models.BigIntegerField()
    buyingToken = models.TextField()
    expiryDate = models.TextField()
    physicalAsset = models.BooleanField()


class Block(models.Model):
    index = models.BigIntegerField()
    merkleRoot = models.TextField()
    previousHash = models.TextField(null=True)
    difficulty = models.BigIntegerField()
    nonce = models.BigIntegerField()


class Transaction(models.Model):
    id = models.AutoField(primary_key=True)
    index = models.BigIntegerField(null=True)
    transactionHash = models.TextField()
    smartContract = models.TextField(null=True)
    timeStamp = models.TextField()
    parentBlock = models.ForeignKey(
        'Block', on_delete=models.CASCADE, null=True)


class Input(models.Model):
    index = models.BigIntegerField()
    blockNumber = models.BigIntegerField()
    TransactionHash = models.TextField()
    outputIndex = models.BigIntegerField()
    signature = models.TextField()
    parentTransaction = models.ForeignKey(
        'Transaction', on_delete=models.CASCADE)


class Output(models.Model):
    id = models.AutoField(primary_key=True)
    index = models.BigIntegerField()
    value = models.BigIntegerField()
    token = models.TextField()
    publicKey = models.TextField()
    parentTransaction = models.ForeignKey(
        'Transaction', on_delete=models.CASCADE)


class BlockChain(models.Model):
    difficulty = models.BigIntegerField()
    trustedPublicKey = models.TextField()
    blockSize = models.BigIntegerField()
    coinToken = models.TextField()
