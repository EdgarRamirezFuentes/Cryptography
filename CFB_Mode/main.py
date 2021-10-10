from classes.CFB_Mode import CFB_Mode

if __name__ == "__main__":
    cfb = CFB_Mode()
    cfb.encrypt("test.txt")
    cfb.decrypt("encrypted.txt", "keys.txt")