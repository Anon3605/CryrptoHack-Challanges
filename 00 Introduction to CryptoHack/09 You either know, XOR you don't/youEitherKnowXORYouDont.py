HexString= "0e0b213f26041e480b26217f27342e175d0e070a3c5b103e2526217f27342e175d0e077e263451150104"
input=bytes.fromhex(HexString[2:])
key= input[0] ^ ord('crypto{')
flag = ''.join(chr(c ^ key) for c in input)

print(flag)