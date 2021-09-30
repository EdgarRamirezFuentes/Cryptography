from Crypto.Cipher import DES3
from Crypto.Util import Padding
from Crypto.Random import get_random_bytes
import math
import base64
import random


def get_permutation ():
    '''
        Generates a permutation for a byte

        Return
        --------
        permutation : list
            It is a list that contains the permutation
    '''
    permutation = list(range(8))
    random.shuffle(permutation)
    return permutation


def bit_is_turned_on (key : bytes, bit_position : int):
    '''
        Check if the ith bit is turned on
        The bit most to the left is the Most Significant Bit

        Parameter
        --------
        key : bytes
            It is the key (byte) that will analyzed to get the status of the ith bit
        
        bit_position : int
            It is the the position of the bit that will be checked
            The bot most to the left has the position 0.
        
        Return 
        --------
        key_value : int
            It is the value of the key after the AND operation.
            If the ith bit was turned off, its value will be 0, otherwise will be different than 0
        
    '''
    return key & 1 << bit_position


def turn_bit_on (key: bytes, bit_position : int):
    '''
        Turn the ith bit of the key on.

        Parameters
        --------
        key : bytes
            It is the key (byte) that will modified
        
        bit_position : int
            bit_position : int
            It is the the position of the bit that will be turned on
            The bot most to the left has the position 0.
    '''
    return key | (1 << bit_position)


def permutate_key (key : bytes, permutation : list):
    '''
        Permutate a key depending on the given permutation

        Parameters
        --------
        key : bytes
            It is the key that will be modified
        
        permutation : list
            It is the permutation that will be used to permutate the key

        Return
        --------
        permutated_key : list
            It is the result of permutate the received key
    '''
    key = int.from_bytes(key, "big")
    permutated_key = 0
    for index, value in enumerate(permutation):
        bit_position = 7 - value
        if bit_is_turned_on(key, bit_position) != 0:
            new_bit_position = 7 - index
            permutated_key = turn_bit_on(permutated_key, new_bit_position)
    return permutated_key


def generate_file (filename : str, data : bytes):
    '''
        Creates a new file, encode in base64 the received data, and write the encoded data in the created file

        Paramaeters
        --------------
        filename : str
            It is the name (with extension) that the created file will take
        data : bytes
            It is the data (in bytes) that will be encoded and written in the created file
    '''
    with open(filename, "w") as key_file:
            base64_data = base64.b64encode(data)
            key_file.write(str(base64_data, "utf-8"))


def read_data_file (filename : str):
    '''
        Read the content of the received file

        Parameters
        ----------------
        filename : str
            It is the name of the file (with extension) that contains the desired data
        
        Return
        ----------------
        data : str
            It is the content of the file

    '''
    data = ""
    with open(filename, mode="r") as file:
        data = file.read()
    return data


def read_base64_file(base64_filename : str):
    '''
        Read the base 64 content of the received file, and decode it to bytes

        Parameters
        ----------------
        base64_filename : str
            It is the name of the file (with extension) that contains the desired data
        
        Return
        ----------------
        data : bytes
            It is the obtained content (in bytes) of the file
    '''
    with open(base64_filename, mode="r") as base64_file:
        data = base64.b64decode(bytes(base64_file.read(), "utf-8"))
    return data


def generate_key(length_of_the_key : int):
    '''
        Generate a valid DES3 24 bytes key

        Parameters
        ----------------
        length_of_the_key : int
            It is the number of bytes will be randomly generated as a valid key for Triple DES

        Returns
        ----------------
        key : bytes
            It is the valid key
    '''
    # Generate a valid DES3 24 bytes key
    while True:
        try:
            key = DES3.adjust_key_parity(get_random_bytes(length_of_the_key))
            break
        except ValueError:
            pass
    return key


def add_padding(data : bytes):
    '''
        Add padding to the byte message if it is necessary
        Note: CBC splits the data in blocks of size 8
        Parameters
        ----------------
        data : bytes
            It is the data (in bytes) that will be encrypted

        Return
        ----------------
        data : bytes
            It is the data with the needed padding added
    '''
    if len(data) % 8 != 0:
        data_length = len(data)
        padding = (8 * (math.floor(data_length / 8 + 1))) - data_length
        # Add the necessary padding to the data
        data += bytes((" " * padding), "utf-8")
    return data


def EDE_encryption(data_filename : str):
    '''
        Encrypt the content of the desired file, create a file that contains the key used to encrypt the data, create a file that contains the encrypted content, and create a file that contains the 
        initialization vector of the encryption cipher.

        Parameters
        ----------------
        data_filename : str
            It is the name of the file that contains the data that will be encrypted
    '''
    data = bytes(read_data_file(data_filename).strip(), "utf-8")
    data = add_padding(data)
    encryption_key = generate_key(24)
    key_filename = input("Input the filename (add the .txt extension) of the file where the key will be stored (Example: data_key.txt): ")
    generate_file(key_filename, encryption_key)

    EDE_cipher = DES3.new(encryption_key, DES3.MODE_CBC)
    encrypted_data  = EDE_cipher.encrypt(data)
    generate_file(data_filename + ".des", encrypted_data)

    initialization_vector_filename = input("Input the filename (add the .txt extension of the file where the initialization vector will be stored (Example: initialization_vector.txt): ")
    generate_file(initialization_vector_filename, EDE_cipher.iv)


def EDE_decryption(encrypted_data_filename : str, key_filename : str, initialization_vector_filename : str):
    '''
        Decrypt the content of the desired file, get the decryption key from the desired file, get the initialization vector from the desired file, and create a file that contains the
        decrypted data

        Parameters
        ----------------
        encrypted_data_filename : str
            It is the name of the file that contains the encrypted data

        key_filename : str
            It is the name of the file that contains the decryption file

        initialization_vector_filename : str
            It is the name of the file that contains the initialization vector
    '''
    encrypted_data = read_base64_file(encrypted_data_filename)
    decryption_key = read_base64_file(key_filename)
    initialization_vector = read_base64_file(initialization_vector_filename)
    EDE_decipher = DES3.new(decryption_key, DES3.MODE_CBC, initialization_vector)
    decrypted_data = EDE_decipher.decrypt(encrypted_data)
    decrypted_data_filename = input("Input the filename (add the .txt extension) of the file where the decrypted data will be stored (Example: decrypted_data.txt): ")
    with open(decrypted_data_filename, mode="w") as decrypted_data_file:
        decrypted_data_file.write(decrypted_data.decode("utf-8"))


if __name__ == "__main__":
    pass