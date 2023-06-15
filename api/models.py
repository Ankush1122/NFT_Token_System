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