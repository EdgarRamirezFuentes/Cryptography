from Crypto.Cipher import DES3
from Crypto.Random import get_random_bytes
import math
# Generate a valid DES3 24 bytes key
while True:
    try:
        key = DES3.adjust_key_parity(get_random_bytes(24))
        break
    except ValueError:
        pass

# Create a DES3 cipher object to encrypt the message.
# The DES3 cipher mode operation will be Cipher-Block Chaining (CBC)
# CBC Mode only accepts 8*n bytes
encryption_cipher = DES3.new(key, DES3.MODE_CBC)

# The CBC mode only accepts 8*n bytes to be encrypted
# It DOES NOT accept strings

# Get the message
plaintext = input("Message: ")

# Add padding to the message if it is necessary
if len(plaintext) % 8 != 0:
    plaintext_length = len(plaintext)
    padding = (8 * (math.floor(plaintext_length / 8 + 1))) - plaintext_length
    # Add the padding to the plaintext
    plaintext += " " * padding
    
# Converting from string to bytes
plaintext = bytes(plaintext, 'utf-8')

encrypted_message = encryption_cipher.encrypt(plaintext)
print(f"Encrypted message: {encrypted_message}")

# Create a DES3 cipher object to decrypt the message
# In this case, it will get as parameter the key used to encrypt the message, 
# the mode used to encrypt the message, and the initialization vector used
# used in the encryption object
decryption_cipher = DES3.new(key, DES3.MODE_CBC, encryption_cipher.iv)
decrypted_message = decryption_cipher.decrypt(encrypted_message)

# Converting from bytes to string
decrypted_message = decrypted_message.decode('utf-8')
print(f"Original message: {decrypted_message}")