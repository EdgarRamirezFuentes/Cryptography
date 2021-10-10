from classes.CBC_Mode import CBC_Mode

if __name__ == "__main__":
    cbc = CBC_Mode()
    cbc.encrypt("test.txt")
    cbc.decrypt("encrypted.txt", "keys.txt")