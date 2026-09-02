<h1 align="center">ASCII</h1>

Here we see ASCII values being turned back into characters, an integer (the
**ordinal**) mapped to the character it stands for, using `chr(value)`.

---

## Where this sits in cryptography

Three categories worth keeping straight, because CTF categories and real
engagements both branch on them:

| Type | Reversible? | Secret needed? |
|---|---|---|
| Encoding | yes | **nopeee** |
| Hashing | nopeee (one-way) | nopeee |
| Encryption / decryption | yes | yes — a key |

The middle column is what people notice. The **right** column is what matters.
Encoding is reversible *by anyone*, which is why "the credentials were
base64-encoded" is written up as plaintext storage, not as weak crypto.

---

## 1. Encoding

Changing the representation of data using a published, keyless algorithm:
character->ASCII, ASCII → binary/octal/hex, bytes → Base64/Base58.

Python builtins:

| Function | Purpose | `99` → |
|---|---|---|
| `ord()` | character → integer | — |
| `chr()` | integer → character | `'c'` |
| `bin()` | integer → binary string | `'0b1100011'` |
| `oct()` | integer → octal string | `'0o143'` |
| `hex()` | integer → hex string | `'0x63'` |

Note the **prefixes**. `hex(99)` returns `'0x63'`, not `'63'`, so a stray `0x`
will break `bytes.fromhex()` later. When building hex strings use format specs
instead:

```python
f"{99:02x}"          # '63'
bytes([99,114]).hex()  # '6372'
```

**Base58** belongs here too — an encoding, not a hash. It drops visually
ambiguous characters (`0`, `O`, `I`, `l`) and is used for Bitcoin addresses and
IPFS CIDs.

## 2. Hashing

Maps arbitrary-length input to a **fixed-length** digest. It is not
"irreversible" as a magic property: because the output is fixed-length and the
input is not, the function **cannot be injective** — preimages exist in
abundance. What makes it one-way is that *finding* one is computationally
infeasible.

That distinction is the practical one. Password cracking and rainbow tables
never invert a hash; they search the plausible input space and compare digests.

| Family | Members | Status |
|---|---|---|
| MD5 | 128-bit | broken — collisions trivial |
| SHA-1 | 160-bit | broken — SHAttered, 2017 |
| SHA-2 | SHA-224/256/384/512 | current standard |
| SHA-3 | SHA3-224/256/384/512 (Keccak) | current standard |
| BLAKE2/BLAKE3 | variable | fast, modern |

"Broken" above means *collisions have been found*, not *reversed*.

There is no `sha32`, `sha58`, or `sha128`. `SHA-2` is a family name, not a
callable algorithm so better use `hashlib.sha256`, and so on.

## 3. Encryption/Decryption

Reversible, but only with a key. Split by whether both parties hold the *same*
key:

**Symmetric** means one shared secret encrypts and decrypts.
Examples: **AES**, DES, 3DES, ChaCha20, RC4.

**Asymmetric** (public-key) means a public key encrypts, a mathematically related
private key decrypts.
Examples: **RSA**, ECC, ElGamal, Diffie–Hellman (key exchange).

Here what I learned in a hard way and I think I should share this:
*Block cipher* and *stream cipher* are not algorithms — they are the two shapes
a symmetric cipher can take. AES and DES are block ciphers (fixed-size input
blocks, hence modes like CBC and CTR); ChaCha20 and RC4 are stream ciphers.

The **Caesar cipher** is a symmetric substitution cipher whose key is a shift
amount. Brute force is the *attack* on it, not the cipher itself — with only 25
non-trivial keys the whole keyspace is searchable by hand.

---

## The challenge

Only encoding, a list of ASCII values, no key involved.

```python
intArray = [99, 114, 121, 112, 116, 111, 123, 65, 83, 67, 73, 73, 95,
            112, 114, 49, 110, 116, 52, 98, 108, 51, 125]

flag = "".join(chr(i) for i in intArray)
print(flag)
```

```
crypto{ASCII_pr1nt4bl3}
```

Mapping the first few by hand against an ASCII table:

```
 99 -> 'c'        123 -> '{'
114 -> 'r'         65 -> 'A'
121 -> 'y'         83 -> 'S'
112 -> 'p'         67 -> 'C'
116 -> 't'         73 -> 'I'
111 -> 'o'         95 -> '_'
```

`chr()` over the list in a generator expression is all it takes so `str.join`
consumes it without any issues, so no intermediate list is built.

---

## Ranges worth memorising

Recognising these on sight saves time on every later challenge:

| Range (hex) | Range (dec) | Contents |
|---|---|---|
| `0x00–0x1F` | 0–31 | control characters (non-printable) |
| `0x20` | 32 | space |
| `0x30–0x39` | 48–57 | digits `0`–`9` |
| `0x41–0x5A` | 65–90 | uppercase `A`–`Z` |
| `0x61–0x7A` | 97–122 | lowercase `a`–`z` |
| `0x7F` | 127 | DEL |

Bit 5 (`0x20`) is the case bit: `'a' ^ 0x20 == 'A'`. Bit 7 is always `0` in
7-bit ASCII — which is why any byte above `0x7F` signals raw binary rather than
text, and why `.decode('utf-8')` throws on it.