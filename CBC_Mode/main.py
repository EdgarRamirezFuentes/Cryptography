'''
	Name: main.py
	Laboratory 3 - Modes of operation
    Authors: 
		* María José Salmerón Contreras 
		* Edgar Alejandro Ramírez Fuentes

    Using Vigenere cipher and CBC Mode encipher and decipher a 500 characters text (English alphabet).
'''

from classes.CBC_Mode import CBC_Mode

if __name__ == "__main__":
    cbc = CBC_Mode()
    print("Choose the operation you want to do \n1. Encipher textfile \n2. Decipher textfile")
    operation = int(input(""))
    if operation == 1:
        filename = input("Input the filename (with extension) that contains the plaintext: ")
        cbc.encrypt(filename)
    elif operation == 2:
        encrypted_filename = input("Input the filename (with extension) that contains the encrypted text: ")
        keys_filename = input("Input the filename (with extension) that contains the keys: ")
        cbc.decrypt(encrypted_filename, keys_filename)
    else:
        print("Wrong option")