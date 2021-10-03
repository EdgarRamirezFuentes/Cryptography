

from typing import Counter


class VigenereCipher:
    '''
        This class is used to encrypt/decrypt text using the Vigenere cipher
    '''
    def __init__ (self):
        self.__alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.__letter_to_index = dict(zip(self.__alphabet, range(len(self.__alphabet))))
        self.__index_to_letter = dict(zip(range(len(self.__alphabet)), self.__alphabet))


    def __divide_text(self, text : str, division_size : int):
        '''
            Divide a text into blocks of size division_key.\n
            Example:\n
            text     |  division_size | result\n
            "abc"   |       3       |  [[0,1,2]]\n
            "abcd" |        3      |  [[0,1,2], [3]]

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
        for index in range(0, len(text), division_size):
            divided_text.append([letter for letter in text[index : index + division_size]])
        return  divided_text


    def encrypt(self, plaintext : str, key : str):
        '''
            Encrypt a plaintext using the key

            Parameters
            --------
            plaintext : str
                It is the plaintext that will be encrypted
            
            key : str
                It is the key used to encrypt the text

            Return
            --------
            encrypted_text : str
                It is  result of encrypting the plaintext using the key
        '''
        encrypted_text = ""
        plaintext_divisions = self.__divide_text(plaintext, len(key))
        for division in plaintext_divisions:
            for i in range(len(division)):
                text_letter = division[i]
                key_letter = key[i]            
                new_text_letter_index = (self.__letter_to_index[text_letter] + self.__letter_to_index[key_letter]) % len(self.__alphabet)
                encrypted_text += self.__index_to_letter[new_text_letter_index]
        return encrypted_text


    def decrypt(self, encrypted_text : str, key : str):
        '''
            Decrypt a encrypted text using the key

            Parameters
            --------
            encrypted_text : str
                It is the encrypted text that will be encrypted
            
            key : str
                It is the key used to decrypt the text

            Return
            --------
            decrypted_text : str
                It is  result of decrypting the encrypted text using the key
        '''
        decrypted_text = ""
        encrypted_text_division = self.__divide_text(encrypted_text, len(key))
        for division in encrypted_text_division:
            for i in range(len(division)):
                text_letter = division[i]
                key_letter = key[i]            
                new_text_letter_index = (self.__letter_to_index[text_letter] - self.__letter_to_index[key_letter]) % len(self.__alphabet)
                decrypted_text += self.__index_to_letter[new_text_letter_index]
        return decrypted_text

if __name__ == "__main__":
    cipher = VigenereCipher()
    key = "cat"
    plaintext = "cryptography"
    encrypted_text = cipher.encrypt(plaintext, key)
    print(encrypted_text)
    print(cipher.decrypt(encrypted_text, key))
