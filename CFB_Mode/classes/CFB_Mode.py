from .VigenereCipher import VigenereCipher
import random
import textwrap
import base64
import math

class CFB_Mode:
    def __init__(self):
        self.__iv = self.__charGenerator(10)
        self.__key = self.__charGenerator(10)
        pass


    def get_key(self):
        
        return self.__key
    
    
    def get_iv(self):
        return self.__iv
    
    
    def __clean_text(self, text : str):
        text = text.replace(' ', '')
        text = text.replace(' ','')
        text = text.replace('\n','')
        text = text.replace('.','')
        text = text.replace(',','')
        text = text.lower()
        return text
    
    
    def __charGenerator(self, size : int):
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        random_key = ""
        for i in range(size):
            random_key += random.choice(alphabet)
        return random_key
    
    
    def __paddingProcess(self, plaintext : str):
        plaintext = plaintext.strip()
        if len(plaintext) % len(self.__iv) != 0:
            plaintext_length = len(plaintext)
            padding = (len(self.__iv) * (math.floor(plaintext_length / len(self.__iv) + 1))) - plaintext_length
			# Add the padding to the plaintext
            plaintext += ("*" * padding)
        return plaintext
    
    
    def __read_plaintext(self, filename : str):
        with open(filename, "r") as reader:
            plaintext = reader.read()
            plaintext = self.__clean_text(plaintext)
            plaintext = self.__paddingProcess(plaintext)
            plaintext = textwrap.wrap(plaintext, len(self.__iv))
        return plaintext
    
    def encrypt(self, filename : str):
        # Get the pĺaintext in blocks
        plaintext = self.__read_plaintext(filename)
        # Transform the initialization vector from char to int
        iv = self.__iv
        vigenere_cipher = VigenereCipher()
        for block in plaintext:
            iv = vigenere_cipher.encrypt(iv, self.__key)
            # Transform from letter to int (ascii)
            block = [ord(letter) for letter in block]
            
            # XOR process
            for index, letter in enumerate(block):
                block[index] ^= ord(iv[index])
        
        
    
    
    