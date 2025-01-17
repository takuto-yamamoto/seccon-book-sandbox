def KSA(key: bytes):
    """
    Key Scheduling Algorithm
    内部状態Sを鍵keyに応じて動的にシャッフルする
    すなわち鍵を内部状態に変換する
    """
    S = list(range(256))
    j = 0

    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]

    return S


def PRGA(S: list[int]):
    """
    Pseudo-Random Generation Algorithm
    KSAで生成した内部状態を元に、内部状態のかき混ぜと1バイトの乱数出力を繰り返す
    この乱数と平文をXORしたものが暗号文になる
    """
    S = S[:]
    i, j = 0, 0

    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        key = S[(S[i] + S[j]) % 256]
        yield key


def xor(a, b):
    return a ^ b


plaintext = b"helloworld"
S = KSA(b"testkey")
ciphertext = bytes(map(xor, plaintext, PRGA(S)))
print(ciphertext)

decrypted_text = bytes(map(xor, ciphertext, PRGA(S)))
print(decrypted_text)
