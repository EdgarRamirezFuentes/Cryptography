'''
    Hash functions laboratory

    Main function

    Authors:
    - Ramírez Fuentes Edgar Alejandro
    - Salmerón Contreras María José
'''
import base64

from classes.HashFunction import HashFunction

if __name__ == "__main__":
    print("Block size: 8")
    hash1 = HashFunction(8)
    hash1.hash_data("./textfiles/data.txt")

    print("\nBlock size: 16")
    hash2 = HashFunction(16)
    hash2.hash_data("./textfiles/data.txt")

    print("\nBlock size: 32")
    hash3 = HashFunction(32)
    hash3.hash_data("./textfiles/data.txt")
    
    # If the block size is not a power of 2, the default block size is 8
    print("\nBlock size: 64")
    hash4 = HashFunction(64)
    hash4.hash_data("./textfiles/data.txt")
    '''
    data = ['AB', 'CD']
    digest = [0 for i in range(len(data[0]))]
    for i in data:
        binary_representation = ''
        for j in i:
            binary_representation += format(ord(j), 'b')
            print(binary_representation)
        print(f"binary {binary_representation} integer {int(binary_representation, 2)}")
    '''

