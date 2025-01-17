import hashlib
import string


def brute_force():
    prefix = "CTF_"

    i = 0

    while True:
        charactors = string.ascii_letters + string.digits

        for char in charactors:
            word = prefix + char
            hash = hashlib.sha1(word.encode()).hexdigest()

            if hash[-3:] == "000":
                print(f"OK: {word} のハッシュ値は {hash}です")
                return
            else:
                print(f"NG: {word}")

        prefix += charactors[i]
        i += 1


if __name__ == "__main__":
    brute_force()
