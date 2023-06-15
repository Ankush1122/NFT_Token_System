import hashlib
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.exceptions import InvalidSignature


class Output:
    __index = None
    __value = None
    __token = None
    __publicKey = None

    def __init__(self, index, value, token, publicKey) -> None:
        self.__index = index
        self.__value = value
        self.__token = token
        self.__publicKey = publicKey

    def getHash(self) -> str:
        return hashlib.sha224(str(self).encode('utf-8')).hexdigest()

    def __str__(self) -> str:
        return str(self.__index) + str(self.__value) + str(self.__token) + str(self.__publicKey)

    def getIndex(self):
        return self.__index

    def getValue(self):
        return self.__value

    def getPublicKey(self):
        return self.__publicKey

    def getToken(self):
        return self.__token

    def verifySignature(self, signature):
        public_key_after = serialization.load_pem_public_key(
            data=self.__publicKey,
            backend=default_backend()
        )
        res = bytes(self.getHash(), 'utf-8')
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
