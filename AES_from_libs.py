from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import hashlib
import os

def get_key(bytes: int=32):
    return get_random_bytes(bytes)

def convert_bytes_to_int(byteString: bytes):
    integerLst = list(map(str, byteString))
    return " ".join(integerLst)

def convert_int_to_bytes(ints: str):
    return bytes(map(int, ints.split(" ")))

def get_file_name(type: str):
    return str(input(f"{type} File... "))

def convert_text_to_bytes(passString: str):
    return hashlib.sha256(passString.encode()).digest()

def encrypt_file(targetFile: str, key: bytes, encryptedFileName: str="encrypted_file.txt"):
    if encryptedFileName == None:
        encryptedFileName = "encrypted_file.txt"

    cipher = AES.new(key, AES.MODE_GCM)

    with open(targetFile, "rb") as file:
        data = file.read()

    encryptedText, tag = cipher.encrypt_and_digest(data)

    with open(encryptedFileName, "wb") as file:
        file.write(cipher.nonce)
        file.write(tag)
        file.write(encryptedText)

def decrypt_file(key: bytes, encryptedFileName: str="encrypted_file.txt", decryptedFileName: str="decrypted_file.txt"):
    if encryptedFileName == None:
        encryptedFileName = "encrypted_file.txt"
    
    if decryptedFileName == None:
        decryptedFileName = "decrypted_file.txt"
    
    with open(encryptedFileName, "rb") as file:
        nonce = file.read(16)
        tag = file.read(16)
        encryptedText = file.read()

    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce)
    try:
        plainText = cipher.decrypt_and_verify(encryptedText, tag)
    except:
        return False

    with open(decryptedFileName, "wb") as file:
        file.write(plainText)
    
    return True

def encrypt_main():
    while True:
        targetFile = get_file_name("Target")
        if os.path.exists(fr"{targetFile}"):
            break
        else:
            print("File does not exist")

    encryptedFile = get_file_name("(leave blank to skip) Encrypted")
    if encryptedFile == "" or encryptedFile == " ":
        print("\nDefaulting Encrypted File to encrypted_file.txt\n")
        encryptedFile = None

    while True:
        keyType = str(input("Key Type - Random (R), Numbers (N), Password (P), Bytes(B))... "))
        if keyType == "R" or keyType == "r":
            print("\nDefaulting to random key\n")
            key = get_key()
            inputString = None
            break
        elif keyType == "N" or keyType == "n":
            try:
                inputString = str(input("Custom Key (32 nums, 0-255)... "))
                key = convert_int_to_bytes(inputString)
                break
            except:
                print("\nInvalid key entry\n")
        elif keyType == "P" or keyType == "p":
            try:
                inputString = str(input("Password... "))
                key = convert_text_to_bytes(inputString)
                break
            except:
                print("\nInvalid key entry\n")
        elif keyType == "B" or keyType == "b":
            try:
                key = bytes(str(input("Bytes... ")))
                inputString = None
                break
            except:
                print("\nInvalid key entry\n")
        else:
            print("Invalid Input")

    if inputString != None:
        print(f"Input Key: {inputString}")
    else:
        print(f"Number key: {convert_bytes_to_int(key)}")

    print(f"Key (Bytes): {key}")

    encrypt_file(targetFile=targetFile, key=key, encryptedFileName=encryptedFile, )

def decrypt_main():
    while True:
        targetFile = get_file_name("(leave blank to skip) Encrypted")
        if targetFile == "" or targetFile == " ":
            print("\nDefaulting Encrypted File to encrypted_file.txt\n")
            targetFile = None
            break
        else:
            if os.path.exists(fr"{targetFile}"):
                break
            else:
                print("File does not exist")

    decryptedFile = get_file_name("(leave blank to skip) Decrypted")
    if decryptedFile == "" or decryptedFile == " ":
        print("\nDefaulting Encrypted File to encrypted_file.txt\n")
        decryptedFile = None

    while True:
        keyType = str(input("Key Type - Numbers (N), Password (P), Bytes(B))... "))
        if keyType == "N" or keyType == "n":
            try:
                key = convert_int_to_bytes(str(input("Custom Key (32 nums, 0-255)... ")))
                break
            except:
                print("\nInvalid key entry\n")
        elif keyType == "P" or keyType == "p":
            try:
                key = convert_text_to_bytes(str(input("Password... ")))
                break
            except:
                print("\nInvalid key entry\n")
        elif keyType == "B" or keyType == "b":
            try:
                key = bytes(str(input("Bytes... ")))
                break
            except:
                print("\nInvalid key entry\n")
        else:
            print("Invalid Input")

    if decrypt_file(key=key, encryptedFileName=targetFile, decryptedFileName=decryptedFile) == False:
        print("Incorrect Password")
        return

def encrypt_directory(directory=None, key=None, hidden=False, dirCount=0):
    if directory == None:
        while True:
            targetDirectory = r"{}".format(str(input("Target Directory... ")))
            if os.path.exists(targetDirectory):
                break
            else:
                print("Directory does not exist")
        
        while True:
            keyType = str(input("Key Type - Random (R), Numbers (N), Password (P), Bytes(B))... "))
            if keyType == "R" or keyType == "r":
                print("\nDefaulting to random key\n")
                key = get_key()
                inputString = None
                break
            elif keyType == "N" or keyType == "n":
                try:
                    inputString = str(input("Custom Key (32 nums, 0-255)... "))
                    key = convert_int_to_bytes(inputString)
                    break
                except:
                    print("\nInvalid key entry\n")
            elif keyType == "P" or keyType == "p":
                try:
                    inputString = str(input("Password... "))
                    key = convert_text_to_bytes(inputString)
                    break
                except:
                    print("\nInvalid key entry\n")
            elif keyType == "B" or keyType == "b":
                try:
                    key = bytes(str(input("Bytes... ")))
                    inputString = None
                    break
                except:
                    print("\nInvalid key entry\n")
            else:
                print("Invalid Input")

        if inputString != None:
            print(f"Input Key: {inputString}")
        else:
            print(f"Number key: {convert_bytes_to_int(key)}")

        print(f"Key (Bytes): {key}")

        while True:
            print("Hide File Names? (make sure there are no text files called 'names.txt' or 'names_encrypted.txt') - Y/n")
            hidden = str(input("... "))
            if hidden == "y" or hidden == "Y":
                hidden = True
                break
            elif hidden == "n" or hidden == "N":
                hidden = False
                break
            else:
                print("Invalid Input")

        print("\nWARNING - This will encrypt all files in this and all sub directories\n")
        
        while True:
            answer = str(input("Proceed (P), Quit (Q), back (B)... "))
            if answer == "p" or answer == "P":
                break
            elif answer == "q" or answer == "Q":
                quit()
            elif answer == "b" or answer == "B":
                main()
            else:
                print("Invalid Input")
    else:
        targetDirectory = directory
        key = key

    if hidden:
        currentDir = os.getcwd()
        os.chdir(targetDirectory)
        nameFile = "names.txt"
        folderNameFile = "names2.txt"
        if os.path.exists(folderNameFile) == False:
            with open(folderNameFile, "x") as file:
                pass
        else:
            with open(folderNameFile, "w") as file:
                file.write("")
        
        if os.path.exists(nameFile) == False:
            with open(nameFile, "x") as file:
                pass
        else:
            with open(nameFile, "w") as file:
                file.write("")

    count = 0
    for filename in os.listdir(targetDirectory):
        filePath = os.path.join(targetDirectory, filename)
        if os.path.isfile(filePath) and filename != nameFile:
            extensionIndex = filePath.rfind(".")
            if hidden:
                encryptedFileName = f"{str(count)}_encrypted.txt"
                with open(nameFile, "a") as file:
                    toWrite = filename + "\n"
                    file.write(toWrite)
                count += 1
            else:
                encryptedFileName = filePath[:extensionIndex] + "_encrypted" + filePath[extensionIndex:]
            encrypt_file(filePath, key, encryptedFileName)
            os.remove(filePath)
        elif os.path.isdir(filePath):
            dirCount = encrypt_directory(directory=filePath, key=key, hidden=hidden, dirCount=dirCount)

    if hidden:
        new_folder = targetDirectory[:targetDirectory.rfind("\\")] + "\\" + str(dirCount) + "_encryptedFolder"
        with open(folderNameFile, "a") as file:
            file.write(targetDirectory)
        encrypt_file(folderNameFile, key, "names2_encrypted.txt")
        encrypt_file(nameFile, key, "names_encrypted.txt")
        os.remove(nameFile)
        os.remove(folderNameFile)
        os.chdir(currentDir)
        os.rename(targetDirectory, new_folder)
        
        return dirCount + 1
    
    return 0

def decrypt_directory(directory=None, key=None, hidden=None):
    nameFileEncrypted = "names_encrypted.txt"
    folderNameFileEncrypted = "names2_encrypted.txt"
    nameFile = "names.txt"
    folderNameFile = "names2.txt"
    currentDir = os.getcwd()
    if directory == None:
        while True:
            targetDirectory = r"{}".format(str(input("Target Directory... ")))
            if os.path.exists(targetDirectory):
                break
            else:
                print("Directory does not exist")
        
        while True:
            keyType = str(input("Key Type - Numbers (N), Password (P), Bytes(B))... "))
            if keyType == "N" or keyType == "n":
                try:
                    inputString = str(input("Key (32 nums, 0-255)... "))
                    key = convert_int_to_bytes(inputString)
                    break
                except:
                    print("\nInvalid key entry\n")
            elif keyType == "P" or keyType == "p":
                try:
                    inputString = str(input("Password... "))
                    key = convert_text_to_bytes(inputString)
                    break
                except:
                    print("\nInvalid key entry\n")
            elif keyType == "B" or keyType == "b":
                try:
                    key = bytes(str(input("Bytes... ")))
                    inputString = None
                    break
                except:
                    print("\nInvalid key entry\n")
            else:
                print("Invalid Input")

        while True:
            print("Are the File Names Hidden? - Y/n")
            hidden = str(input("... "))
            if hidden == "y" or hidden == "Y":
                os.chdir(targetDirectory)
                fileExists = os.path.exists(nameFileEncrypted)
                os.chdir(currentDir)
                if fileExists == False:
                    print("Name file not found")
                else:
                    hidden = True
                    break
            elif hidden == "n" or hidden == "N":
                hidden = False
                break
            else:
                print("Invalid Input")

        print("\nWARNING - This will attempt to decrypt all files in this and all sub directories with '_encrypted' before the file extension\n")
        
        while True:
            answer = str(input("Proceed (P), Quit (Q), back (B)... "))
            if answer == "p" or answer == "P":
                break
            elif answer == "q" or answer == "Q":
                quit()
            elif answer == "b" or answer == "B":
                main()
            else:
                print("Invalid Input")
    else:
        targetDirectory = directory
        key = key
        os.chdir(targetDirectory)
        if os.path.exists(nameFileEncrypted) == False:
            print("ERROR! - Name file not found (defaulting to non-hidden)")
            hidden = False            
    
    if hidden:
        os.chdir(targetDirectory)
        if decrypt_file(key=key, encryptedFileName=nameFileEncrypted, decryptedFileName=nameFile) == False:
            print("Incorrect Password")
            return
        if decrypt_file(key=key, encryptedFileName=folderNameFileEncrypted, decryptedFileName=folderNameFile) == False:
            print("Incorrect Password")
            return
        
        with open(nameFile, "r") as file:
            nameLst = file.read().split("\n")
        lastEntry = nameLst[-1]
        if lastEntry == "" or lastEntry == " " or lastEntry == "\n":
            nameLst.pop()

        with open(folderNameFile, "r") as file:
            folderNameLst = file.read().split("\n")
        lastEntry = folderNameLst[-1]
        if lastEntry == "" or lastEntry == " " or lastEntry == "\n":
            folderNameLst.pop()

        # remove files
        os.remove(nameFileEncrypted)
        os.remove(folderNameFileEncrypted)
        os.remove(nameFile)
        os.remove(folderNameFile)

        # rename folder
        os.chdir(currentDir)
        os.rename(targetDirectory, folderNameLst[0])
        targetDirectory = folderNameLst[0]
        os.chdir(targetDirectory)

    for filename in os.listdir(targetDirectory):
        invalid = False
        filePath = os.path.join(targetDirectory, filename)
        if os.path.isfile(filePath) and filename != nameFile and filename != folderNameFile:
            extensionIndex = filePath.rfind(".")
            underscoreIndex = filePath.rfind("_encrypted")
            if underscoreIndex != -1 and extensionIndex != -1:
                if hidden:
                    try:
                        decryptedFileName = os.path.join(targetDirectory, nameLst[int(filename[:filename.rfind("_encrypted")])])
                    except:
                        print(f"Passed unkown file {filename}")
                        invalid = True
                else:
                    decryptedFileName = filePath[:underscoreIndex] + filePath[extensionIndex:]
                if invalid == False:
                    if decrypt_file(key=key, encryptedFileName=filePath, decryptedFileName=decryptedFileName) == False:
                        print("Incorrect Password")
                        return
                    os.remove(filePath)
            else:
                print(f"Passed unkown file {filename}")
        elif os.path.isdir(filePath):
            decrypt_directory(directory=filePath, key=key, hidden=hidden)
    
    if hidden:
        os.chdir(currentDir)

def main():
    while True:
        print("Encrypt - E/e\nDecrypt - D/d\nQuit - Q/q\nEncrypt Directory - ED/ed\nDecrypt Directory - DD/dd")
        answer = str(input("... "))
        if answer == "E" or answer == "e":
            encrypt_main()
        elif answer == "ED" or answer == "ed" or answer == "eD" or answer == "Ed":
            encrypt_directory()
        elif answer == "DD" or answer == "dd" or answer == "dD" or answer == "Dd":
            decrypt_directory()
        elif answer == "D" or answer == "d":
            decrypt_main()
        elif answer == "Q" or answer == "q":
            quit()
        else:
            print("Invalid Input!")


if __name__ == "__main__":
    main()