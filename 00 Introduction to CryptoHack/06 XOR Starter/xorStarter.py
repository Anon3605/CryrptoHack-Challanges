string = "label"

flag = "".join(chr(ord(c) ^ 13) for c in string)
print("crypto{"+flag+"}")