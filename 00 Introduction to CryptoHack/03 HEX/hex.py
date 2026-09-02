hexStrings= "63727970746f7b596f755f77696c6c5f62655f776f726b696e675f776974685f6865785f737472696e67735f615f6c6f747d"

parser = bytes.fromhex(hexStrings)
print(parser)
flag=parser.decode('utf-8')
print(flag)

# for i in range(0, len(hexStrings), 2):
#     print(chr(int(hexStrings[i:i+2], 16)), end="")