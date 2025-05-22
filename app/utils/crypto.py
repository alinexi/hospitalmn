import os
from Crypto.Cipher import DES
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256
from base64 import b64encode, b64decode
from flask import current_app

def _load_des_key():
    """Load DES key from file."""
    key_path = current_app.config['DES_KEY_PATH']
    if not os.path.exists(key_path):
        raise FileNotFoundError(f"DES key not found at {key_path}")
    with open(key_path, 'rb') as f:
        return f.read()

def _load_rsa_keys():
    """Load RSA keys from files."""
    private_key_path = current_app.config['RSA_PRIVATE_KEY_PATH']
    public_key_path = current_app.config['RSA_PUBLIC_KEY_PATH']
    
    if not os.path.exists(private_key_path) or not os.path.exists(public_key_path):
        raise FileNotFoundError("RSA keys not found")
    
    with open(private_key_path, 'rb') as f:
        private_key = RSA.import_key(f.read())
    with open(public_key_path, 'rb') as f:
        public_key = RSA.import_key(f.read())
    
    return private_key, public_key

def encrypt_data(data):
    """Encrypt data using DES."""
    if not data:
        return None
    
    # Convert string to bytes if necessary
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    # Pad data to be multiple of 8 bytes
    padding_length = 8 - (len(data) % 8)
    padded_data = data + bytes([padding_length] * padding_length)
    
    # Create DES cipher
    key = _load_des_key()
    cipher = DES.new(key, DES.MODE_ECB)
    
    # Encrypt and encode
    encrypted = cipher.encrypt(padded_data)
    return b64encode(encrypted).decode('utf-8')

def decrypt_data(encrypted_data):
    """Decrypt data using DES."""
    if not encrypted_data:
        return None
    
    # Decode from base64
    encrypted = b64decode(encrypted_data)
    
    # Create DES cipher
    key = _load_des_key()
    cipher = DES.new(key, DES.MODE_ECB)
    
    # Decrypt and unpad
    decrypted = cipher.decrypt(encrypted)
    padding_length = decrypted[-1]
    unpadded = decrypted[:-padding_length]
    
    return unpadded.decode('utf-8')

def sign_data(data):
    """Sign data using RSA private key and SHA-256."""
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    private_key, _ = _load_rsa_keys()
    hash_obj = SHA256.new(data)
    signature = pkcs1_15.new(private_key).sign(hash_obj)
    return b64encode(signature).decode('utf-8')

def verify_signature(data, signature):
    """Verify signature using RSA public key and SHA-256."""
    if isinstance(data, str):
        data = data.encode('utf-8')
    
    _, public_key = _load_rsa_keys()
    hash_obj = SHA256.new(data)
    signature_bytes = b64decode(signature)
    
    try:
        pkcs1_15.new(public_key).verify(hash_obj, signature_bytes)
        return True
    except (ValueError, TypeError):
        return False

def generate_keys():
    """Generate new DES and RSA keys."""
    # Generate DES key
    des_key = os.urandom(8)
    os.makedirs(os.path.dirname(current_app.config['DES_KEY_PATH']), exist_ok=True)
    with open(current_app.config['DES_KEY_PATH'], 'wb') as f:
        f.write(des_key)
    
    # Generate RSA keys
    key = RSA.generate(2048)
    private_key = key.export_key()
    public_key = key.publickey().export_key()
    
    os.makedirs(os.path.dirname(current_app.config['RSA_PRIVATE_KEY_PATH']), exist_ok=True)
    with open(current_app.config['RSA_PRIVATE_KEY_PATH'], 'wb') as f:
        f.write(private_key)
    with open(current_app.config['RSA_PUBLIC_KEY_PATH'], 'wb') as f:
        f.write(public_key) 