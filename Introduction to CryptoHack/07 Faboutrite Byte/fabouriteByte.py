# hexString=0x73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d
# print(int(hexString))
# # print(bytes.fromhex(hexString)
# bytes = b"sbi`d\x7fk h! O!%O}iOv$f eb!'#Ori'um"
# for i in bytes:
#     string=""
#     for j in str(int(hexString)):
#         string+=str(i^int(j))
#     print(bytes.fromhex(string))
# print(bin(0x7))
# print(int(0x7))
# # 000 0111
# # print(chr(11111000))

# for i in str(int(hexString)):
#     string=""
#     for j in str(int(hexString)):
#         # print(i,j)
#         string+=(str(int(i)^int(j)))
#     print(string)


# Solution: The given hex string represents a ciphertext that has been XORed with a single-byte key. 
# The code iterates through all possible single-byte keys (0-255) and attempts to decode the ciphertext 
# by XORing each byte of the ciphertext with the current key. It prints out the key and the resulting 
# decoded bytes for each iteration.

hex_string = "73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d"

ciphertext = bytes.fromhex(hex_string)

for key in range(256):
    decoded = bytes(c ^ key for c in ciphertext)
    print(key, decoded)

# Solution: The given hex string represents a ciphertext that has been XORed with a single-byte key.
# The code iterates through all possible single-byte keys (0-255) and attempts to decode the 
# ciphertext by XORing each byte of the ciphertext with the current key. It prints out the key and 
# the resulting decoded bytes for each iteration.

input_str = bytes.fromhex('73626960647f6b206821204f21254f7d694f7624662065622127234f726927756d')

key = input_str[0] ^ ord('c')
print(''.join(chr(c ^ key) for c in input_str))