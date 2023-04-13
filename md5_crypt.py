import binascii
import hashlib
import sys

class md5crypt:

    #initial intermediate
    def intermediate_sum(self, password, salt, magic):
        intermediate = password + magic + salt
        alternate = self.alternate_sum(password, salt)
        password_length = len(password)
        hexalternate = binascii.unhexlify(alternate)

        '''
        For each bit in length(password)
        from low to high and stopping after the most significant set bit
        If the bit is set, append a NUL byte
        If it’s unset, append the first byte of the password
        '''
        
        #go from length to 0 in steps of decreasing 16
        for i in range(password_length, 0, -16):
            intermediate += hexalternate[0:16 if i > 16 else i]

        while password_length:
            if password_length & 1:
                intermediate += chr(0).encode()
            else:
                intermediate += password[0:1]
            
            password_length >>= 1

        return hashlib.md5(intermediate).hexdigest()

    # loop through the concatination iterations
    '''
    For i = 0 to 999 (inclusive), compute Intermediatei+1 by concatenating and hashing the following:
    If i is even, Intermediatei
    If i is odd, password
    If i is not divisible by 3, salt
    If i is not divisible by 7, password
    If i is even, password
    If i is odd, Intermediatei
    '''
    def loop(self, intermediate, password, salt):
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
    def get_bytes(self, intermediate):
        response = b""
        byte_list = [11, 4, 10, 5, 3, 9, 15, 2, 8, 14, 1, 7, 13, 0, 6, 12]
        for individual_byte in byte_list:
            response += intermediate[individual_byte:individual_byte + 1]
        
        return response

    #crypt base64 table
    base64="./0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

    def string_to_hex(self, string):
        return binascii.hexlify(string.encode())

    def alternate_sum(self, password, salt):
        return hashlib.md5(password + salt + password).hexdigest()

    def hash(self, password, salt):
        magic = b"$1$"

        #initial intermediate
        intermediate = self.intermediate_sum(password, salt, magic)

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
    
    '''
    file that has every 6 character combination of lowercase letters
    308 million characters
    use generate.sh to create the list of passwords to work on
    ie `./generate 6 > passwords`
    '''
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