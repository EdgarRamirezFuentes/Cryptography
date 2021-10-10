from os import write
from .VigenereCipher import VigenereCipher
import random
import textwrap
import base64
import math

class CFB_Mode:
    def __init__(self):
        '''
            Class used to encipher/decipher text using the CFB Mode
        '''
        self.__iv = self.__generate_key(10)
        self.__key = self.__generate_key(10)
        pass


    def get_key(self):
        '''
            Get the key used for the Vigenere cipher

            Returns
            ------------
            key : str
                It is the key used to encipher/decipher in the Vigenere cipher
        '''
        return self.__key
    
    
    def get_iv(self):
        '''
            Get the initialization vector used for the CFB Mode

            Returns
            ------------
            iv : str
                It is the initialization vector used to encipher/decipher in the CFB Mode
        '''
        return self.__iv
    
    
    def __clean_text(self, text : str):
        '''
			Clean the plaintext to delete characters that do not belong to the english alphabet

			Parameters
			--------------
			text : str
				It is the text that will be cleaned

			Returns
			--------------
			text : str
				It is the text cleaned
		'''
        text = text.replace(' ', '')
        text = text.replace(' ','')
        text = text.replace('\n','')
        text = text.replace('.','')
        text = text.replace(',','')
        text = text.lower()
        return text
    
    
    def __generate_key(self, size : int):
        '''
			Generates a random key base 64

			Parameters
			------------
			size : int
				It is the key size

			Returns
			------------
			random_key : str
				It is the random key generated
		'''
        alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
        random_key = ""
        for i in range(size):
            random_key += random.choice(alphabet)
        return random_key
    
    
    def __add_padding(self, plaintext : str):
        '''
			Add the necessary padding to the plaintext to fulfill the length of the initialization vector

			Parameters
			-------------
			plaintext : str
				It is the plaintext that will be padded

			Returns
			--------------
			plaintext : str
				It is the plaintext with the necessary padding added 
		'''
        plaintext = plaintext.strip()
        if len(plaintext) % len(self.__iv) != 0:
            plaintext_length = len(plaintext)
            padding = (len(self.__iv) * (math.floor(plaintext_length / len(self.__iv) + 1))) - plaintext_length
			# Add the padding to the plaintext
            plaintext += ("*" * padding)
        return plaintext
    
    
    def __read_plaintext(self, filename : str):
        '''	
			Read the plaintext from the textfile provided, add padding if necessary, and divide the plaint text in blocks.

			Parameters
			-------------
			textFile : str
				It is the filename (with extension) that contains the plaintext
    
			Returns
			-------------
			blocks : list
				It is the plaintext divided in blocks
		'''
        with open(filename, "r") as reader:
            plaintext = reader.read()
            plaintext = self.__clean_text(plaintext)
            plaintext = self.__add_padding(plaintext)
            plaintext = textwrap.wrap(plaintext, len(self.__iv))
        return plaintext


    def __read_encrypted_text(self, filename : str):
        '''
			Get the encripted data from the provided file, and divide it in blocks

			Parameters
			-----------------
			filename : str

			Returns
			-----------------
			blocks : list
				It is a list that contains the encrypted blocks
		'''
        with open(filename, "r") as reader:
            encrypted_text = reader.read().split("&")
        return encrypted_text
            


    def __write_text(self, filename : str, text : str):
        '''
			Create a file, and write the text provided in that text

			Parameters
			--------------
			filename : str
				It is the name (with extension) that the new file will get
    
			text : str
				It is the text that will be written in the created file
		'''
        with open(filename, "w") as writer:
            writer.write(text)


    def encrypt(self, filename : str):
        '''
			Encrypt the plaintext from the textfile provided

			Parameters
			-------------
			filename : str
				It is the filename (with extension) that contains the plaintext
		'''

        # Get the pĺaintext in blocks
        plaintext = self.__read_plaintext(filename)
        
        iv = self.__iv

        # Store the keys needed to decrypt the message
        self.__write_text("keys.txt", self.__iv + "&" + self.__key)

        # Store the encrypted text
        encrypted_text = ""

        vigenere_cipher = VigenereCipher()

        for block in plaintext:

            iv = vigenere_cipher.encrypt(iv, self.__key)

            # Transform from letter to int (ascii)
            block = [ord(letter) for letter in block]
            
            # XOR process
            for index in range(len(block)):
                block[index] ^= ord(iv[index])

            # Transform the result of the XOR operation to base 64
            block = base64.standard_b64encode(bytes(block))
        
            # Base 64 always adds == at the end of the transformation
			# Delete the last == 
            block = block.decode()[:-2]

            # Update the iv value to encrypt the next block
            iv = block

            # Add & to split each block in the decryption process
            encrypted_text += block + "&"

            # Store the encrypted text without the last &
            self.__write_text("encrypted.txt", encrypted_text[:-1])
            


    def decrypt(self, encrypted_filename : str, keys_filename : str):
        '''
			Decrypt the encrypted text from the textfile provided

			Parameters
			-------------
			encrypted_filename : str
				It is the filename (with extension) that contains the encrypted text

			keys_filename : str
				It is the filename (with extension) that contains the keys to decrypt the text
		'''
        # Store the encrypted text divided in blocks
        encrypted_text = self.__read_encrypted_text(encrypted_filename)

        keys = self.__read_encrypted_text(keys_filename)

        # Store the decrypted text
        decrypted_text = ""
        
        # Store the initialization vector
        iv = keys[0]
        # Store the vigenere key used to encrypt the plaintext
        vigenere_key = keys[1]

        vigenere_cipher = VigenereCipher()

        for block in encrypted_text:
            # Store the encrypted block to use it to decrypt the next block
            ci = block

            # Reverse base 64
            block = base64.standard_b64decode(bytes(block + "==", "utf-8")).decode("utf-8")

            # Tranform Ci from letters to int (ascii)
            block = [ord(letter) for letter in block]

            # Cipher the iv to XOR it with Ci
            iv = vigenere_cipher.encrypt(iv, vigenere_key)

            # XOR process
            for index in range(len(block)):
                block[index] ^= ord(iv[index])
            
            # Update the iv to decryp the next block
            iv = ci

            # Concatenate the decrypted block to the decrypted text
            for letter in block:
				# Transform from int to char
                decrypted_text += chr(letter)
            
            # Write the decripted text in a textfile
            self.__write_text("decrypted.txt", decrypted_text)




    