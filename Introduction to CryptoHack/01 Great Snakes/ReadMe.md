<h1 align="center">Great Snakes</h1>
We have this

```python
ords = [81, 64, 75, 66, 70, 93, 73, 72, 1, 92, 109, 2, 84, 109, 66, 75, 70, 90, 2, 92, 79]
```

21 integers. understanding *why* the operation reverses, not in breaking anything.

---

## The two builtins

| Function | Direction | Example |
|---|---|---|
| `ord(c)` | character → integer | `ord('c')` → `99` |
| `chr(n)` | integer → character | `chr(99)` → `'c'` |

`ord` returns the **ord**inal (code point). `chr` builds a **char**acter.
There is no `char()` builtin in Python — that's the C name.

In Python 3 these operate on Unicode code points, but below 128 that is
identical to ASCII, so it doesn't matter here.

---

## First attempt: decode straight to ASCII

```python
print("".join(chr(i) for i in ords))
```

Gives us output:

```
Q@KBF]IH\x01\m\x02TmBKFZ\x02\O
```

Not a flag. Two things to notice before moving on:

- 21 input values, but only **18 printable characters**. The values `1`, `2`, `2`
  are control characters (SOH, STX) that a terminal renders as nothing.
  Copy-pasting terminal output silently drops them.
- The printable part is heavy on uppercase letters and punctuation, which is a
  hint that a single bit near the top of each byte has been flipped.

---

## The key

```
50  =  0x32  =  0b00110010
```

(`0x32` is also the ASCII code for the character `'2'` — a small joke on the 
challenge author's part.)

---

## XOR

Bitwise addition mod 2 — addition with the carry chain removed.

| a | b | a ^ b |
|---|---|---|
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

Same bits → `0`. Different bits → `1`.

Worked example on the first byte:

```
        dec   hex     binary
 C       81   0x51   0101 0001
 key     50   0x32   0011 0010
        ---   ----   ---------  XOR, no carry propagation
 p       99   0x63   0110 0011   -> chr(99) = 'c'
```

Compare with `81 + 50 = 131`, where a carry cascades out of bit 1. That carry
chain is what makes addition awkward to invert. XOR has none.

---

## Why one operation does both directions

XOR is **self-inverse**: `a ^ a == 0` for every `a`, and `a ^ 0 == a`.
Combined with associativity:

```
(p ^ k) ^ k  =  p ^ (k ^ k)  =  p ^ 0  =  p
```

So the encoder and the decoder are the same line of code. There is no separate
inverse function to write. Modular addition, by contrast, needs `+k` one way and
`-k` the other.

---

## Recovering the key if it weren't given

Not needed here, but this is the actual lesson. Apply the same cancellation to
the ciphertext relation:

```
C     = p ^ k
C ^ p = (p ^ k) ^ p = (p ^ p) ^ k = 0 ^ k = k
```

CryptoHack flags always start with `crypto{`, so one known character is enough:

```python
>>> 81 ^ ord('c')
50
```

That's an equation with a unique solution, not a guess. A single matched
plaintext/ciphertext byte **determines** the key byte. This is a crib attack, and
it works regardless of how large the key space is — the 256-value space of
single-byte XOR isn't even the main weakness.

---

## Solution

```python
ords = [81, 64, 75, 66, 70, 93, 73, 72, 1, 92, 109, 2, 84, 109, 66, 75, 70, 90, 2, 92, 79]

print("".join(chr(o ^ 0x32) for o in ords))
```

```
We get this: crypto{z3n_0f_pyth0n}
```

The commented-out `import this` at the top of the challenge file is the hint
pointing at the Zen of Python.

---

## What the control characters were telling us

`0x32` has bits set at positions 1, 4, and 5.

Bit 5 (`0x20`) is the ASCII case bit — flipping it drags lowercase letters from
`0x61–0x7A` down into the `0x41–0x5A` range. That is why `'c'` (`0x63`) appeared
as `'Q'` (`0x51`), and why the raw decode looked like uppercase and punctuation.

The tiny values are more revealing. ASCII digits live at `0x30–0x39`, sharing
their upper nibble with the key:

```
'3' = 0x33 ^ 0x32 = 0x01
'0' = 0x30 ^ 0x32 = 0x02
```

XOR annihilates the shared bits and collapses digits into the control range. So
`1` and `2` in the ciphertext are a signal that the plaintext contains digits
*and* that the key's upper nibble is `0x3` — before decrypting anything.
Structure survives XOR. That is the whole vulnerability.

---

## Takeaway OR Notes

The identity that actually matters:

```
C1 ^ C2 = (p1 ^ k) ^ (p2 ^ k) = p1 ^ p2
```

The key cancels completely. XOR two ciphertexts encrypted under the same
keystream and you get the XOR of the plaintexts, with zero knowledge of the key
and regardless of its length. This is the many-time-pad attack — the reason
keystream reuse breaks stream ciphers (WEP IV collisions, CTR-mode nonce reuse,
Venona).

For repeating-key XOR the chain follows directly: recover keysize by normalized
Hamming distance across blocks, transpose into columns that each share one key
byte, then solve every column as this single-byte problem via frequency scoring.

Everything breakable here is a violated one-time-pad condition — key as long as
the message, uniformly random, never reused. Satisfy all three and the identical
XOR operation becomes information-theoretically secure.