from Crypto.Cipher import DES, DES3
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import base64
import random
import sys


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


def is_bit_turned_on (key : bytes, bit_position : int):
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
        permutated_key : bytes
            It is the result of permutate the received key
    '''
    try:
        # Transform the bytes key into an int key to be able to manipulate its bits
        key = int.from_bytes(key, "big")
        # This is going to be the new key, which will contain all the permutations
        permutated_key = 0
        print("Original key: ")
        for i in range(7, -1, -1):
            print("0", end="") if is_bit_turned_on(key, i) == 0 else print("1", end="")
        
        print(f"\nPermutation list {permutation}")
        for index, value in enumerate(permutation):
            bit_position = 7 - value
            # Only turn a bit on if necessary
            if is_bit_turned_on(key, bit_position) != 0:
                new_bit_position = 7 - index
                permutated_key = turn_bit_on(permutated_key, new_bit_position)
        # Return the permutated key as bytes
        print("Permutated key: ")
        for i in range(7, -1, -1):
            print("0", end="") if is_bit_turned_on(permutated_key, i) == 0 else print("1", end="")
        return permutated_key.to_bytes(1, "big")
    except:
        print("Something went wrong")
        sys.exit()


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
    try:
        with open(filename, "w") as key_file:
                base64_data = base64.b64encode(data)
                key_file.write(str(base64_data, "utf-8"))
    except:
        print("Something went wrong")
        sys.exit()


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
    try:
        data = ""
        with open(filename, mode="r") as file:
            data = file.read()
        return data
    except:
        print("Something went wrong")
        sys.exit()


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
    try:
        with open(base64_filename, mode="r") as base64_file:
            data = base64.b64decode(bytes(base64_file.read(), "utf-8"))
        return data
    except:
        print("Something went wrong")
        sys.exit()


def generate_key(length_of_the_key : int):
    '''
        Generate a valid DES3 24 bytes key, and create the text file that contains the encryption key

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
            key_filename = input("Input the filename (add the .txt extension) of the file where the key will be stored (Example: data_key.txt): ")
            generate_file(key_filename, key)
            break
        except:
            print("Something went wrong")
            sys.exit()
    return key


def EDE_encryption(data_filename : str):
    '''
        Encrypt the content of the desired file, create a file that contains the key used to encrypt the data.
        Note: This data is encrypted using the EDE variant of Triple DES.
        Parameters
        ----------------
        data_filename : str
            It is the name of the file that contains the data that will be encrypted
    '''
    try:
        data = pad(bytes(read_data_file(data_filename).strip(), "utf-8"), 8)
        encryption_key = generate_key(24)
        EDE_cipher = DES3.new(encryption_key, DES3.MODE_ECB)
        encrypted_data  = EDE_cipher.encrypt(data)
        generate_file(data_filename + ".des", encrypted_data)
    except:
        print("Something went wrong")
        sys.exit()


def EDE_decryption(encrypted_data_filename : str, key_filename : str):
    '''
        Decrypt the content of the desired file, get the decryption key from the desired file, and create a file that contains the decrypted data\n
        Note: This data is decrypted using the EDE variant of Triple DES. Thus, the content of the file must have been encrypted using the EDE variant of Tiple DES.
        Parameters
        ----------------
        encrypted_data_filename : str
            It is the name of the file that contains the encrypted data

        key_filename : str
            It is the name of the file that contains the decryption file
    '''
    try:
        encrypted_data = read_base64_file(encrypted_data_filename)
        decryption_key = read_base64_file(key_filename)
        EDE_decipher = DES3.new(decryption_key, DES3.MODE_ECB)
        decrypted_data = EDE_decipher.decrypt(encrypted_data)
        decrypted_data_filename = input("Input the filename (add the .txt extension) of the file where the decrypted data will be stored (Example: decrypted_data.txt): ")
        # Write the decrypted data (with no padding) in the text file
        with open(decrypted_data_filename, mode="w") as decrypted_data_file:
            decrypted_data_file.write(unpad(decrypted_data, 8).decode("utf-8"))
    except:
        print("Something went wrong")
        sys.exit()


def EEE_encryption(data_filename : str, ):
    '''
        Encrypt the content of the desired file, create a file that contains the key used to encrypt the data, and create a file that contains the encrypted content.
        Note: This data is encrypted using the EEE variant of Triple DES.
        Parameters
        ----------------
        data_filename : str
            It is the name of the file that contains the data that will be encrypted
    '''
    try:
        data = pad(bytes(read_data_file(data_filename).strip(), "utf-8"), 8)
        encryption_key = get_random_bytes(8)
        key_filename = input("Input the filename (add the .txt extension) of the file where the key will be stored (Example: data_key.txt): ")
        generate_file(key_filename, encryption_key)
        EEE_cipher = DES.new(encryption_key, DES.MODE_ECB)
        #  Encryption process
        E1  = EEE_cipher.encrypt(data)
        cipher = DES.new(encryption_key, DES.MODE_ECB)
        E2 = cipher.encrypt(E1)
        cipher2 = DES.new(encryption_key, DES.MODE_ECB)
        E3 = cipher2.encrypt(E2)
        generate_file(data_filename + ".des", E3)
    except:
        print("Something went wrong")
        sys.exit()


def EEE_decryption(encrypted_data_filename : str, key_filename : str):
    '''
        Decrypt the content of the desired file, get the decryption key from the desired file, and create a file that contains the decrypted data\n
        Note: This data is decrypted using the EEE variant of Triple DES. Thus, the content of the file must have been encrypted using the EEE variant of Tiple DES.
        Parameters
        ----------------
        encrypted_data_filename : str
            It is the name of the file that contains the encrypted data

        key_filename : str
            It is the name of the file that contains the decryption file
    '''
    try:
        encrypted_data = read_base64_file(encrypted_data_filename)
        decryption_key = read_base64_file(key_filename)
        decipher = DES.new(decryption_key, DES.MODE_ECB)
        # Decryption process
        D1 = decipher.decrypt(encrypted_data)
        decipher2 = DES.new(decryption_key, DES.MODE_ECB)
        D2 = decipher2.decrypt(D1)
        decipher3 = DES.new(decryption_key, DES.MODE_ECB)
        D3 = decipher3.decrypt(D2)
        decrypted_data_filename = input("Input the filename (add the .txt extension) of the file where the decrypted data will be stored (Example: decrypted_data.txt): ")
        # Write the decrypted data (with no padding) in the text file
        with open(decrypted_data_filename, mode="w") as decrypted_data_file:
            decrypted_data_file.write(unpad(D3, 8).decode("utf-8"))
    except:
        print("Something went wrong")
        sys.exit()


if __name__ == "__main__":
    print("Lab 2b. DES/3DES")
    print("Ramirez Fuentes Edgar Alejandro")
    print("First let try the permutate key function")
    print("The permutation table must follow the next format: 5,3,7,0,2,1,4,6")
    permutation_table =[int(permutation)  for permutation in input("Enter the permutation table: ").split(",")]
    permutate_key(get_random_bytes(1), permutation_table)
    print("\n\nNow let's try to encrypt a text file using 3DES using the variant EDE")
    plaintext_filenme = input("Enter the filename (adding the .txt extension) that contains the data that will be encrypted: ")
    print("Your data is being encrypted")
    EDE_encryption(plaintext_filenme)
    print("\n\nTwo text files were generated, and those are crtitical to decrypt the message.")
    print("\nThe file that constains the encrypted data is named using this format: fileame.txt.des\nThe file that contains the decryption key was named by you, and has the following format: filename.txt")
    print("\n\nNow let's try to decrypt the previous encrypted dataa using the variant EDE")
    encrypted_text_filename = input("Enter the filename (adding the .txt.des extension) that contains the encrypted data: ")
    decryption_key_filename = input("Enter the filename (adding the .txt extension) that contains the decryption key: ")
    print("Your data is being decrypted")
    EDE_decryption(encrypted_text_filename, decryption_key_filename)

    print("\n\nNow let's try to encrypt a text file using 3DES using the variant EEE")
    plaintext_filenme = input("Enter the filename (adding the .txt extension) that contains the data that will be encrypted: ")
    print("Your data is being encrypted")
    EEE_encryption(plaintext_filenme)
    print("\n\nTwo text files were generated, and those are crtitical to decrypt the message.")
    print("\nThe file that constains the encrypted data is named using this format: fileame.txt.des\nThe file that contains the decryption key was named by you, and has the following format: filename.txt")
    print("\n\nNow let's try to decrypt the previous encrypted dataa using the variant EEE")
    encrypted_text_filename = input("Enter the filename (adding the .txt.des extension) that contains the encrypted data: ")
    decryption_key_filename = input("Enter the filename (adding the .txt extension) that contains the decryption key: ")
    print("Your data is being decrypted")
    EEE_decryption(encrypted_text_filename, decryption_key_filename)