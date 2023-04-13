import binascii
import hashlib
import sys

class md5crypt:

    #initial intermediate
    def get_intermediate(self, password: str, salt: str, magic: str) -> str:
        intermediate = password + magic + salt
        alternate = self.get_alternate(password, salt)
        passwd_length = len(password)

        xalternate = binascii.unhexlify(alternate)
        for i in range(passwd_length, 0, -16):
            intermediate += xalternate[0:16 if i > 16 else i]

        while passwd_length:
            if passwd_length & 1:
                intermediate += chr(0).encode()
            else:
                intermediate += password[0:1]
            
            passwd_length >>= 1

        return hashlib.md5(intermediate).hexdigest()

    # loop through the concatination iterations
    def loop(self, intermediate: bytes, password: str, salt: str) -> str:
        for i in range(1000):
            alternate = b""
            if i & 1: 
                alternate += password
            else: 
                alternate += intermediate
            if i % 3: 
                alternate += salt
            if i % 7: 
                alternate += password
            if i & 1: 
                alternate += intermediate
            else: 
                alternate += password

            intermediate = hashlib.md5(alternate).digest()

        return intermediate

    #rearrange bytes by given list
    def get_bytes(self, intermediate: bytes) -> bytes:
        response = b""
        byte_list = [11, 4, 10, 5, 3, 9, 15, 2, 8, 14, 1, 7, 13, 0, 6, 12]
        for individual_byte in byte_list:
            response += intermediate[individual_byte:individual_byte + 1]
        
        return response

    #crypt base64 table
    base64="./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    def string_to_hex(self, string: str) -> str:
        return binascii.hexlify(string.encode())

    def get_alternate(self, password: str, salt: str) -> str:
        return hashlib.md5(password + salt + password).hexdigest()

    def hash(self, password: bytes, salt: bytes) -> str:
        magic = b"$1$"

        #initial intermediate
        intermediate = self.get_intermediate(password, salt, magic)

        # loop through the concatination iterations
        intermediate = self.loop(binascii.unhexlify(intermediate), password, salt)

        # rearrange bytes by given list
        intermediate = self.get_bytes(intermediate)

        # hex to int
        intermediate = int(binascii.hexlify(intermediate), 16)

        # int to base64
        encoded = ""
        for _ in range(22):
            encoded += self.base64[intermediate % 64]
            intermediate //= 64

        return magic.decode() + salt.decode() + '$' + encoded

if __name__ == "__main__":

    #the hash taken from etc_shadow, team42
    expected_hash = "$1$4fTgjp6q$XJ4b7w1UQni3YpIwY2/99/"
    
    #file that has every 6 character combination of lowercase letters
    #308 million characters
    #use generate.sh to create the list of passwords to work on
    #ie `./generate 6 > passwords`
    file = open("passwords")
    
    #the salt retrieved from the hash
    salt = b"4fTgjp6q"

    #helps track how many hashes have been ran through
    hash_counter = 1

    instance = md5crypt()

    for line in file:

        #encode turns the password from the file into bytes
        #rstrip removes the trailing new line
        password = line.encode().rstrip()
        MD5 = instance.hash(password, salt)
        hash_counter+= 1
        if MD5 == expected_hash:
            print("password is: ", line)
            break
        else:
            print(line, MD5, hash_counter)
        
        






        


        

