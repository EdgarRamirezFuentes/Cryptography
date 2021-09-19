import math

class HillCipher:
    def __init__(self, alphabet):
        '''
            Hill Cipher

            Parameters
            ------------------------
            alphabet : list
                It is the alphabet used for encryption/decryption in the Hill Cipher
        '''
        self.__alphabet = alphabet
    
    def extended_euclidean_algorithm(self, x):
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
        u = x
        v = len(self.__alphabet) 
        x1 = 1
        x2 = 0
        while u != 1:
            q = math.floor(v/u)
            r = v - q * u
            x = x2 - q * x1
            v = u
            u = r
            x2 = x1
            x1 = x
        return int(x1 % len(self.__alphabet))

