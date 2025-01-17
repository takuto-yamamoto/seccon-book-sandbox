N = 177773


def factor(n: int):
    factors: list[int] = []
    i = 2
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)

    if n > 1:
        factors.append(n)

    return factors


if __name__ == "__main__":
    factors = factor(N)
    print(factors)
