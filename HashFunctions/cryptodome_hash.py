'''
    Hash functions laboratory

    Use SHA3 512 provided by PyCryptodome to hash images and textfiles

    Authors:
    - Ramírez Fuentes Edgar Alejandro
    - Salmerón Contreras María José
'''

from Crypto.Hash import SHA3_512

if __name__ == '__main__':
    
    # Hashing an image
    with open('./images/meme.jpg', "rb") as image:
        meme_bytes = image.read()

    hash = SHA3_512.new()
    hash.update(meme_bytes)
    print(f"Image digest: {hash.hexdigest()}")

    # Hashing a textfile
    with open('./textfiles/data.txt', 'r') as textfile:
        textfile_bytes = bytes(textfile.read(), 'utf-8')
    
    hash2 = SHA3_512.new()
    hash2.update(textfile_bytes)
    print(f"Textfile digest: {hash2.hexdigest()}")