# Commutative: A ⊕ B = B ⊕ A
# Associative: A ⊕ (B ⊕ C) = (A ⊕ B) ⊕ C
# Identity: A ⊕ 0 = A
# Self-Inverse: A ⊕ A = 0

# import Crypto.util.number as number

KEY1 = int(0xa6c8b6733c9b22de7bc0253266a3867df55acde8635e19c73313)
KEY2xorKEY1 = int(0x37dcb292030faa90d07eec17e3b1c6d8daf94c35d4c9191a5e1e)
KEY2xorKEY3 = int(0xc1545756687e7573db23aa1c3452a098b71a7fbf0fddddde5fc1)
FLAGxorKEY1xorKEY3xorKEY2 = int(0x04ee9855208a2cd59091d04767ae47963170d1660df7f56f5faf)

KEY2 = (KEY1) ^ (KEY2xorKEY1)
KEY3 = (KEY2) ^ (KEY2xorKEY3)

FLAG = (KEY1) ^ (KEY2) ^ (KEY3) ^ (FLAGxorKEY1xorKEY3xorKEY2)
print(bytes.fromhex(f"{FLAG:x}").decode())
