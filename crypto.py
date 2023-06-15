from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Key Generation
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096,
    backend=default_backend()
)
public_key = private_key.public_key()

print(private_key)
print(public_key)


# Serialization
password = "uZV3lwfCADw3X8A9XXENN5QYSvmgHvyB"
password_bytes = password.encode('utf-8')

pem_private = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.BestAvailableEncryption(password_bytes)
)
pem_public = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

# Load Encrypted keys from file
print(type(pem_public))
private_key_after = serialization.load_pem_private_key(
    data=pem_private,
    password=password_bytes,
    backend=default_backend()
)

public_key_after = serialization.load_pem_public_key(
    data=pem_public,
    backend=default_backend()
)

print(public_key_after)
print(private_key_after)

# Signing
p1 = rsa.generate_private_key(
    public_exponent=65537,
    key_size=4096,
    backend=default_backend()
)
p2 = p1.public_key()

message = "hello world!"
res = bytes(message, 'utf-8')

signature = private_key_after.sign(
    res,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)

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
    print("wrong public key")
else:
    print("signature verified")
