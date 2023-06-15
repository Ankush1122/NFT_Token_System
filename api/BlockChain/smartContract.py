import hashlib


class smartContract:
    __id = None
    __sellerPublicKey = None
    __sellingAmount = None
    __sellingToken = None
    __buyerPublicKey = None
    __buyingAmount = None
    __buyingToken = None
    __expiryDate = None
    __physicalAsset = None

    def __init__(self, id, sellerPublicKey, sellingAmount, sellingToken, buyerPublicKey, buyingAmount, buyingToken, expiryDate, physicalAsset) -> None:
        self.__id = id
        self.__sellerPublicKey = sellerPublicKey
        self.__sellingAmount = sellingAmount
        self.__sellingToken = sellingToken
        self.__buyerPublicKey = buyerPublicKey
        self.__buyingAmount = buyingAmount
        self.__buyingToken = buyingToken
        self.__expiryDate = expiryDate
        self.__physicalAsset = physicalAsset

    def getHash(self) -> str:
        return hashlib.sha256(str(self).encode('utf-8')).hexdigest()

    def __str__(self) -> str:
        return str(self.__id) + str(self.__sellerPublicKey) + str(self.__sellingAmount) + str(self.__sellingToken) + str(self.__buyerPublicKey) + str(self.__buyingAmount) + str(self.__buyingToken) + str(self.__expiryDate) + str(self.__physicalAsset)

    def getId(self):
        return self.__id

    def getSellerPublicKey(self):
        return self.__sellerPublicKey

    def getSellingAmount(self):
        return self.__sellingAmount

    def getSellingToken(self):
        return self.__sellingToken

    def getBuyerPublicKey(self):
        return self.__buyerPublicKey

    def getBuyingAmount(self):
        return self.__buyingAmount

    def getBuyingToken(self):
        return self.__buyingToken

    def getExpiryDate(self):
        return self.__expiryDate

    def getPhysicalAsset(self):
        return self.__physicalAsset
