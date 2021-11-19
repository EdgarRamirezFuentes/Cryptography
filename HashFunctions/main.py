'''
    Hash functions laboratory

    Main function

    Authors:
    - Ramírez Fuentes Edgar Alejandro
    - Salmerón Contreras María José
'''

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
    print("\nBlock size: 2")
    hash4 = HashFunction(1)
    hash4.hash_data("./textfiles/data.txt")
