'''
    Author: María José Salmerón Contreras & Edgar Alejandro Ramírez Fuentes
    LABORATORY 3.
    Using Vigenere cipher and CBC Mode encipher and decipher a 500 characters text (English alphabet).
'''
#from Crypto.Cipher.DES3 import block_size
#from Crypto.Random import get_random_bytes
import math
import textwrap
import random
from .VigenereCipher import VigenereCipher
import base64

class CBC_Mode:
    
	def __init__(self):
		'''
			Class used to encipher decipher text using the CBC Mode
		'''
		self.__iv = self.__charGenerator(10)
		# Key used for Vigenere cipher
		self.__key = None


	def get_key(self):
		'''
			Get the key used for Vigenere cipher

			Returns
			---------------
			key : str
				It is the key used for Vigenere cipher
		'''
		return self.__key


	def get_iv(self):
		'''
			Get the initialization vector used for CBC Mode

			Returns
			---------------
			iv : str
				It is the initialization vector used for CBC Mode
		'''
		return self.__iv


	def __cleanText(self, text : str):
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
		text = text.replace(' ','')
		text = text.replace('\n','')
		text = text.replace('.','')
		text = text.replace(',','')
		text = text.lower()
		return text


	def __read_plaintext(self, textFile : str):
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
		with open(textFile ,'r', encoding="utf-8") as textfile_data:
			blocks=[]
			plaintext = textfile_data.read()
			plaintext = self.__cleanText(plaintext)
			# Add padding to the message if it is necessary
			plaintext= self.__paddingProcess(plaintext)
			blocks = textwrap.wrap(plaintext, len(self.__iv))
			return blocks


	def __read_encrypted_data(self, filename : str):
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
			return reader.read().split("&")


	def __paddingProcess(self, plaintext : str):
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
		plaintext= plaintext.strip()
		if len(plaintext) % len(self.__iv) != 0:
			plaintext_length = len(plaintext)
			padding = (len(self.__iv) * (math.floor(plaintext_length / len(self.__iv) + 1))) - plaintext_length
			# Add the padding to the plaintext
			plaintext += ("*" * padding)
		return plaintext


	def __charGenerator(self, size : int):
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
		# Base 64 alphabet
		alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
		random_key = ""
		for i in range(size):
			random_key += random.choice(alphabet)
		return random_key

	def __writeText(self, filename : str, text : str):
		'''
			Create a file, and write the text provided in that text

			Parameters
			--------------
			filename : str
				It is the name (with extension) that the new file will get
    
			text : str
				It is the text that will be written in the created file
		'''
		with open(filename, 'w') as writer:
			writer.write(text)

	def encrypt(self, filename : str):
		'''
			Encrypt the plaintext from the textfile provided

			Parameters
			-------------
			filename : str
				It is the filename (with extension) that contains the plaintext
		'''
		# Plaintext divided in blocks
		plaintext = self.__read_plaintext(filename)
		
		# IV is the value that will be XORed with each block
		iv = self.__iv
		# Store the encrypted text
		encrypted_text = ""

		vigenere_cipher = VigenereCipher()

		for block in plaintext:
			# Transform the block from letters to int
			block = [ord(letter) for letter in block]
			# XOR each int (letter) with iv
			for index in range(len(block)):
				block[index] ^= ord(iv[index])

			# Transform the result of the XOR operation to base 64
			block = base64.standard_b64encode(bytes(block))


			# Base 64 always adds == at the end of the transformation
			# Delete the last == 
			block = block.decode()[:-2]
			
			# Generate a valid key for vigenere and write in a textfile the keys for the decrytion process
			if not self.__key:
				self.__key = self.__charGenerator(len(block))
				keys = self.__iv + "&" + self.__key
				self.__writeText("keys.txt", keys)
			
			# Get Ci
			block = vigenere_cipher.encrypt(block, self.__key)

			# Update iv to be Ci
			iv = block
			
			# Add the & character to split each encrypted block in the decryption process
			block += "&"
			# Concatenate the block to the string that contains all the encrypted blocks
			encrypted_text += block
		# Write the encrypted text in a textfile without the last &
		self.__writeText("encrypted.txt", encrypted_text[:-1])


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
		# Store the decrypted text
		decrypted_text = ""
		# Store the encrypted dat in blocks
		encrypted_data = self.__read_encrypted_data(encrypted_filename)


		with open(keys_filename, "r") as reader:
			# Get the keys 
			keys = reader.read().split("&")
			# IV is the value that will be XORed with each block
			iv = keys[0]
			# Store the key used in vigenere
			key = keys[1]

		vigenere_cipher = VigenereCipher()

		for block in encrypted_data:
			# It is encrypted block that will be used in the next steps to decrypt the next blocks
			ci = block
			# Get the original base 64 value and transform it in bytes
			block = bytes(vigenere_cipher.decrypt(block, key) + "==", "utf-8")
			# Decode the base 64 text
			block = base64.standard_b64decode(block).decode("utf-8")
			# Transform from char to int to XOR with iv
			block = [ord(letter) for letter in block]
			# XOR each int (character) with iv
			for index in range(len(block)):
				block[index] ^= ord(iv[index])
			# iv takes the value of c1 to decrypt the next blocks
			iv = ci
			# Concatenate each letter obtained to the decrypted text
			for letter in block:
				# Transform from int to char
				decrypted_text += chr(letter)
		# Write the decrypted text in a textfile
		self.__writeText("decrypted.txt", decrypted_text)


