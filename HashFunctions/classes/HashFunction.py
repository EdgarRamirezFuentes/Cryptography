'''
    Hash functions laboratory

    Implementation of a hash function using the XOR operation
    This version only hashes the content of a textfile

    Authors:
    - Ramírez Fuentes Edgar Alejandro
    - Salmerón Contreras María José
'''

import textwrap
import random

class HashFunction:
    '''
        Hash function class used to hash only characters contained in the Extended ASCII code
    '''
    def __init__(self, block_size : int = 8) -> None:
        '''
            Initialize the HashFunction object

            Parameters
            ----------
            block_size : int
                It represents the block size and It must be a power of 2. If it is not a power of 2, its value will be 8.

        '''

        ''' 
            If block size is a power of 2, block_size & (block_size - 1) = 0
            e.g 6 and 8
            6 = 110 5 = 101, 110 & 101 = 100
            8 = 1000 7 = 0111, 1000 & 0111 = 0000
        '''
        self.__block_size = block_size if block_size >= 8 and ( (block_size & (block_size - 1)) == 0) else 8


    def get_block_size(self):
        '''
            Get the block size of the hash function

            Return
            -------

            block_size : int 
                It is the current block size of the hash function
        '''
        return self.__block_size


    def __get_data(self, textfile : str) -> str:
        '''
            Get the data contained in the provided textfile

            Parameters
            ----------
            textfile : str
                It is the filename (with extension) that contains the data
            
            Returns
            ---------
            data : str
                It is the data contained in the textfile

        '''
        with open(textfile, 'r') as file:
            data = file.read()
        return data


    def hash_data(self, filenme : str) -> None:
        '''
            Hash the data contained in the textfile using the XOR Operation, and print the digest

            Parameters
            ------------

            filename : str
                It is the filename (with extension) that contains the data to be hashed
        '''
        # Get the data from the textfile with padding added if necessary to fulfill the block size
        data = self.__get_blocks(self.__get_data(filenme))

        # The resulting digest
        digest = 0
        
        # Process each block of the data to hash it
        for block in data:
            digest ^= self.__block_to_bits(block)
        print("Digest")
        self.__digest_to_binary(digest)
        self.__digest_to_hexadecimal(digest)


    def __block_to_bits(self, block : str):
        '''
            Transform a block of characters to its bits representation
            
            Parameters
            -----------
            block : str 
                It is the characters contained in the block to be converted to its bits representation
                
            Returns
            ----------
            integer_representation : int
                It is the integer that represents the bits representation
            
            
        '''
        # Store the bits representation in string
        binary_representation = ''
        for character in block:
            # Get the binary representation of the ASCII character value and oncatenate it ot the block bits representation
            binary_representation += format(ord(character), 'b')
        '''
            Store the integer value that belongs to the bits representation
            e.g
            block = "AB"
            A = 65 = 1000001
            B = 66 = 1000010
            bits representation of the block = 10000011000010
            integer = 8386
        '''
        integer_representation = int(binary_representation, 2)
        return integer_representation


    def __get_blocks(self, data : str) -> list:
        '''
            Divide the data provided in block to process them in the hash function
            
            Parameters
            ----------
            
            data : str
                It is the data that will be divided in blocks
                
            Returns
            --------
            
            data : list 
                It is a list of strings that represent the blocks to be processed in the hash function
        '''
        char_per_block = self.__block_size // 8
        data = textwrap.wrap(data, char_per_block)
        # Add padding to the last block if necessary
        if len(data[-1]) < char_per_block:
            # Concatenate the missing characters to fulfill the blocksize
            data[-1] += '.' * (char_per_block - len(data[-1]))
        return data


    def __digest_to_hexadecimal(self, digest : int) -> None:
        '''
            Print the hexadecimal n blocks representation of the digest

            Parameters
            -----------
            digest : int
                It is the digest to be transformed
        '''
        # Get the necessary digits in hexadecimal to fulfill the hash block
        hexadecimal_length = self.__block_size // 4
        '''
            hex() return string that contains a hexadecimal number using the format 0x40
            We only need the digits after 0x
        '''
        hexadecimal_representation = hex(digest)[2:]
        # Get the remaining hexadecimal digits, which are 0's, to fulfill the block size
        remaining_digits = hexadecimal_length - len(hexadecimal_representation)
        # Hexadecimal reprentation that fulfills the block size
        print(f"Hexadecimal {self.__block_size} blocks representation: 0x{'0'*(remaining_digits)}{hexadecimal_representation}")


    def __digest_to_binary(self, digest : int) -> None:
        '''
            Print the binary n blocks representation of the digest

            Parameters
            -----------
            digest : int
                It is the digest to be transformed
        '''
        binary_representation = format(digest, 'b')
        # Remaining 0's to fulfill the block size
        remaining_bits = self.__block_size - len(binary_representation)
        print(f"Binary {self.__block_size} blocks representation: {'0'* remaining_bits}{binary_representation}")