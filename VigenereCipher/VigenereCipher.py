class VigenereCipher:
    '''
        This class is used to encrypt/decrypt text using the Vigenere cipher
    '''
    def __init__ (self):
        self.__alphabet = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        self.__letter_to_index = dict(zip(self.__alphabet, range(len(self.__alphabet))))
        self.__index_to_letter = dict(zip(range(len(self.__alphabet)), self.__alphabet))


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
        for i in range(len(plaintext)):
            text_letter = plaintext[i]
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
        for i in range(len(encrypted_text)):
            text_letter = encrypted_text[i]
            key_letter = key[i]            
            new_text_letter_index = (self.__letter_to_index[text_letter] - self.__letter_to_index[key_letter]) % len(self.__alphabet)
            decrypted_text += self.__index_to_letter[new_text_letter_index]
        return decrypted_text

if __name__ == "__main__":
    cipher = VigenereCipher()
    print(cipher.encrypt("cry", "cat"), cipher.encrypt("pto", "cat"))
    print(cipher.decrypt("err", "cat"), cipher.decrypt("rth", "cat"))