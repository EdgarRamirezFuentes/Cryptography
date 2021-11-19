'''
    Hash functions laboratory

    Implementation of a hash function using the XOR operation

    Authors:
    - Ramírez Fuentes Edgar Alejandro
    - Salmerón Contreras María José
'''
class HashFunction:
    '''
        Hash function class used to hash characters contained in the Extended ASCII code
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

            If these 
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


    def __set_bit(self, position : int, bits : int) -> int:
        '''
            Set the bit placed in the given position in the provided bits string.

            Parameters
            -----------
            position : int
                It represents the bit position that will be set

            bits : int
                It is the bits string that will be modified

            Returns
            -----------
            bits : int
                It is the modified bits string
        '''
        bits |= (1 << position)
        return bits


    def __unset_bit(self, position : int, bits : int) -> int:
        '''
            Unset the bit placed in the given position in the provided bits string.

            Parameters
            -----------
            position : int
                It represents the bit position that will be unset

            bits : int
                It is the bits string that will be modified

            Returns
            -----------
            bits : int
                It is the modified bits string
        '''
        bits &= ~(1 << position)
        return bits


    def __get_bit_state(self, position : int, bits : int) -> int:
        '''
            Get the bit state in the given position in the provided bits string

            Parameters
            -----------
            position : int
                It represents the bit position that will be checked

            bits : int
                It is the bits string that contains the bit

            Returns
            -----------
            bits : int
                It is the bit status.
        '''
        bits &= (1 << position)
        return bits

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
    
    # XOR function from scratch using 
    def __XOR(self, digest : int, block : int):
        '''
            XOR the current digest of the hash function with the block provided

            Parameter
            -----------

            digest : int 
                It is the current digest of the hash function

            Return : int
                It is the result of XOR digest with the block provided 
        '''
        for bit_position in range(self.__block_size):
            '''
                If the bits have the same status, that bit will be unset, otherwise the bit will be set
                1 XOR 1 = 0
                0 XOR 0 = 0
                1 XOR 0 = 1
                0 XOR 1 = 1
            '''
            # Get the status of the bit at the current position
            digest_bit_status = 0 if not self.__get_bit_state(bit_position, digest) else 1
            block_bit_status = 0 if not self.__get_bit_state(bit_position, block) else 1

            digest = self.__set_bit(bit_position, digest) if (digest_bit_status != block_bit_status) else self.__unset_bit(bit_position, digest)
        return digest
    

    def hash_data(self, filenme : str) -> None:
        '''
            Hash the data contained in the textfile using the XOR Operation, and print the digest

            Parameters
            ------------

            filename : str
                It is the filename (with extension) that contains the data to be hashed
        '''
        # Get the data from the textfile
        data = self.__get_data(filenme)

        # The resulting digest
        digest = 0

        # Each letter is a block
        for letter in data:
            letter_ascii = ord(letter)
            '''
                Use the XOR operation built from scratch
            digest = self.__XOR(digest, letter_ascii)
            '''
            # XORing each bit of the current block with the digest
            digest = (digest ^ letter_ascii)
        
        print("Resulting digest")
        print(f"Binary representation: {format(digest, 'b')}")
        print(f"Hexadecimal representation: {hex(digest)} ")
        # Print the blocks that are 0's eg. 3 with a block size of 8 = 0x03
        self.__digest_to_binary(digest)
        # Print the unset bits before the most significant bit eg. 3 with a block size of 8 = 00000011
        self.__digest_to_hexadecimal(digest)


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