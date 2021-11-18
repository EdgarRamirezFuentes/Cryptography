class HashFunction:
    '''
        TODO: 
        * Implement the hash function
        * Implement a way two show the digest in its hexadecimal representation
    '''

    '''
        Hash function class used to hash characters contained in the Extended ASCII code
    '''
    def __init__(self, block_size : int) -> None:
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
        self.block_size = block_size if block_size >= 8 and ( (block_size & (block_size - 1)) == 0) else 8


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