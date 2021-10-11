'''
	Name: VigenereCipher.py
	Laboratory 3 - Modes of operation
    Authors: 
		* María José Salmerón Contreras 
		* Edgar Alejandro Ramírez Fuentes

    Using Vigenere cipher and CFB Mode encipher and decipher a 500 characters text (English alphabet).
'''
import textwrap

class VigenereCipher:
    '''
        This class is used to encrypt/decrypt text in base 64 using the Vigenere cipher
    '''
    def __init__ (self):
        # Alphabet base 64
        self.__alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        self.__letter_to_index = dict(zip(self.__alphabet, range(len(self.__alphabet))))
        self.__index_to_letter = dict(zip(range(len(self.__alphabet)), self.__alphabet))


    def encrypt(self, letters : str, key : str):
        '''
            Encrypt a plaintext in base 64 using the key provided

            Parameters
            --------
            plaintext : str
                It is the plaintext in base 64 that will be encrypted
            
            key : str
                It is the key used to encrypt the text

            Return
            --------
            encrypted_text : str
                It is  result of encrypting the plaintext using the key
        '''
        encrypted_text = ""
        # Split up the letters in blocks of size of the key
        letters = textwrap.wrap(letters, len(key))
        for block in letters:
            for index, letter in enumerate(block):
                key_index = self.__letter_to_index[key[index]]
                letter_index = self.__letter_to_index[letter]
                encrypted_text += self.__index_to_letter[(letter_index + key_index) % len(self.__alphabet)]
        return encrypted_text


    def decrypt(self, letters : str, key : str):
        '''
            Decrypt a encrypted text in base 64 using the key

            Parameters
            --------
            encrypted_text : str
                It is the encrypted text in base 64 that will be encrypted
            
            key : str
                It is the key used to decrypt the text

            Return
            --------
            decrypted_text : str
                It is  result of decrypting the encrypted text using the key
        '''
        decrypted_text = ""
        for index, letter in enumerate(letters):
            key_index = self.__letter_to_index[key[index]]
            letter_index = self.__letter_to_index[letter]
            decrypted_text += self.__index_to_letter[(letter_index - key_index) % len(self.__alphabet)]
        return decrypted_text
