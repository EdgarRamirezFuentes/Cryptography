'''
    Name: Hill Cipher
    
    Description:
    This class is used to encrypt/decrypt a message using the Hill Cipher
    
    Author: Edgar Ramírez
    
    GitHub: https://github.com/EdgarRamirezFuentes

    Last update: 09/20/2021
'''

import math
import numpy as np
import sympy as sp
import random

class HillCipher:
    '''
        This class is used to encrypt/decrypt plaintext using the Hill Cipher
    '''
    def __init__(self, alphabet):
        '''
            Hill Cipher class constructor

            Parameters
            ------------------------
            alphabet : string
                It is the alphabet used for encryption/decryption in the Hill Cipher
        '''
        self.__alphabet = alphabet
        self.__letter_to_index = dict(zip(self.__alphabet, range(len(self.__alphabet))))
        self.__index_to_letter = dict(zip(range(len(self.__alphabet)), alphabet))
    
    def __extended_euclidean_algorithm(self, x : int) -> int:
        '''
            Calculate the multiplicative inverse of x.

            Parameters
            ---------------------------
            x : int
                It is a number that belongs to Zn where n is the size of the alphabet

            Return
            ---------------------------
            int
                This is the multiplicative inverse of x
        '''
        size_of_alphabet = len(self.__alphabet)
        u = x
        v = size_of_alphabet 
        x1 = 1
        x2 = 0
        try:
            while u != 1:
                q = math.floor(v/u)
                r = v - q * u
                x = x2 - q * x1
                v = u
                u = r
                x2 = x1
                x1 = x
        except:
            return -1

        return int(x1 % size_of_alphabet)

    def decrypt_message(self, filename : str, size_of_the_key : int):
        '''
            Decrypt a encrypted message (using the inverse matrix of the Hill Cipher key) from the data got from the text file and show the original message

            Parameters
            -------------------
            filename : str
                It is name of the text file that contains the necessary data to decrypt the message
            
            size_of_the_key : int
                It defines the size of the square key matrix.
        '''
        size_of_the_alphabet = len(self.__alphabet)
        # data[ciphertext, encryption key, size of the message without padding]
        data = self.__get_data(filename, size_of_the_key)
        ciphertext = data[0]
        print(f"The encrypted message is: {ciphertext}")
        encryption_key = sp.Matrix(data[1])
        determinant_value = sp.det(encryption_key)
        inverse_matrix = encryption_key.inv()
        # Get the multiplicative inverse between the determinant of the encryption key and the size of the alphabet
        multiplicative_inverse = self.__extended_euclidean_algorithm(determinant_value)
        decryption_key = np.array((multiplicative_inverse * (determinant_value * inverse_matrix)) % size_of_the_alphabet)
        # Divide the cipher the into blocks to decrypt each block
        divided_ciphertext = self.__divide_text(ciphertext, size_of_the_key)
        plaintext = ""
        # Size of the message withou padding
        size_of_the_plaintext = data[2]
        # Decrypt each generated block using the decryption mkey
        for i in divided_ciphertext:
            multiply_matrix = None
            multiply_matrix = np.matmul(np.array(i), decryption_key) % size_of_the_alphabet
            for index in multiply_matrix:
                # Add the decrypted characters to the plaintext
                plaintext += self.__index_to_letter[index]
        # Show the decrypted message without padding
        print(f"The decrypted message is: {plaintext[:size_of_the_plaintext]}")


    def __divide_text(self, text : str, division_size : int) -> list:
        '''
            Divide a text into blocks that contain division_size integers, which are the indexes of the characters in the alphabet. It adds random numbers as padding to the last block if it is needed\n
            Example:\n
            text     |  division_size | result\n
            "abc"   |       3       |  [[0,1,2]]\n
            "abcd" |        3      |  [[0,1,2], [3,4,1]] -> 4,1 are random integers used as padding\n

            Parameters
            --------------
            text : str
                It is the text that will be divided
            
            division_size : int
                It defines the size of each block created.
            
            Return
            ---------------
            list[list[int]]
                It is a matrix that contains each block generated from the text
        '''
        divided_text = list()
        current_division = 0
        for index in range(0, len(text), division_size):
            divided_text.append([self.__letter_to_index[letter] for letter in text[index : index + division_size]])
            current_division_size = len(divided_text[current_division])
            if current_division_size < division_size:
                for i in range(division_size - current_division_size):
                    divided_text[current_division].append(random.randint(1, 5))
            current_division += 1
        return  divided_text


    def encrypt_message(self, plaintext : str, size_of_the_key : int):
        '''
            Encrypt the plaintext and create a text file that contains the information to decrypt the message

            Parameters
            ---------------------
            plaintext : str
                It is the message that will be encrypted by the Hill Cipher.

            size_of_the_key : int
                It defines the size of the square key matrix.
        '''
        size_of_the_alphabet = len(self.__alphabet)
        encryption_key = np.array(self.__generate_encryption_key(size_of_the_key))
        ciphertext = ""
        divided_plaintext = self.__divide_text(plaintext, size_of_the_key)
        for i in divided_plaintext:
            multiplication_matrix = None
            multiplication_matrix = np.matmul(np.array(i), encryption_key) % size_of_the_alphabet
            try:
                for index in multiplication_matrix:
                    ciphertext += self.__index_to_letter[index]
            except KeyError as err:
                print("A character in the plaintext does not belong to the alphabet. The message will not be encrypted")
        
        # Get the filename 
        while(True):
            filename = input("Input the filename where the key and ciphertext will be stored: ")
            print("Filename required") if not filename else print("File created successfully")
            if filename:
                break
        # Create and write in the file data such as the length of the message without padding, ciphertext, and the key
        self.__write_file(filename, ciphertext, encryption_key, len(plaintext))


    def __write_file(self, filename : str, ciphertext : str, encryption_key : list, plaintext_size : int):
        '''
            Create a text file named as filename and write the ciphertext, encryption_key, and plaintext_size using the following format:\n
            5\n
            Ciphertext:\n
            hmlbxt\n
            Key:\n
            2 1 1\n
            5 4 3\n 
            1 4 4\n 
            \n
            Note: The first line is the length of the message without padding

            Parameters
            ------------
            filename : str
                It is the name of the text file that will be created

            ciphertext : str
                It is the encrypted message (It might contain padding characters)

            encryption_key : list[list[int]]
                It is the Hill cipher key used to encrypt the message

            plaintext_size : int
                It is the length of the message without padding if it contains
        '''
        with open(filename + ".txt", "w") as file:
            # Write the length of the message without padding
            file.write(str(plaintext_size) + "\n")
            file.write("Ciphertext:\n")
            # Write the encrypted message with padding if it contains
            file.write(ciphertext + "\n")
            file.write("Key:\n")
            # Write the Hill Cipher key used to encrypt the message in matrix shape
            for row in encryption_key:
                for column in row:
                    file.write(str(column) + " ")
                file.write("\n")


    def __get_data(self, filename : str, size_of_the_key : int):
        '''
            Get the necessary data to decrypt a message from a text file 
            Parameters
            -------------
            filename : str
                It is the name of the text file that contains the necessary information to decrypt a message

            size_of_the_key : int
                It defines the size of the square key matrix.

            Return
            -------------
            list[ str, list[ list[ int ] ], int ]
                It is a list that contains the ciphertext, Hill Cipher key, and the length of the message without padding
        '''
        with open(filename + '.txt', "r") as file:
            plaintext_size = int(file.readline()[:-1])
            file.readline()
            ciphertext = file.readline()[:-1]
            file.readline()
            encryption_key = list()
            for i in range(size_of_the_key):
                row = file.readline()[:-1]
                encryption_key.append([int(number) for number in row.split(" ")[:-1]])
            file.readline()
        return [ciphertext, encryption_key, plaintext_size]


    def __generate_encryption_key(self, size_of_the_key : int) -> list:
        '''
            Generate a valid Hill Cipher square matrix key to encrypt a message\n
            Requirements of a valid Hill Cipher square matrix:
            - Its determinant must belong to Zn where n is the size of the alphabet
            - It must have inverse matrix
            - The great common divisor between its determinant and the size of the alphabet must be 1 in order to get the multiplicative inverse
            
            Parameters
            -------------
            size_of_the_key : int
                It defines the size of the square key matrix.
            
            Return
            ------------
            list[list[int]]
                It is the Hill Cipher key
        '''
        size_of_the_alphabet = len(self.__alphabet)
        while (True):
            encryption_key = [[random.randint(1, 5) for j in range(size_of_the_key)] for i in range(size_of_the_key)]
            # Using the possible Hill Cipher matrix as
            encryption_key_sp = sp.Matrix(encryption_key)
            determinant_value = sp.det(encryption_key_sp)
            if determinant_value > 0 and determinant_value < size_of_the_alphabet and math.gcd(determinant_value, size_of_the_alphabet) == 1:
                break
        return encryption_key


# Section used to test the class
if __name__ == "__main__":
    alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z', ' ']
    cipher = HillCipher(alphabet)
    text = input("Message: ")
    size_of_the_key = int(input("Size of the key: "))
    cipher.encrypt_message(text, size_of_the_key)
    filename = input("Name of the file that cointains the data: ")
    cipher.decrypt_message(filename, size_of_the_key)

