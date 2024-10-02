def _rail_fence_encryption(text: str, key: int, decrypt: bool = False) -> str:
    def encrypt(text: str, key: int) -> str:
        result = ""
        for i in range(key):
            for j in range(i, len(text), key):
                result += text[j]
        return result

    def decrypt(text: str, key: int) -> str:
        result = ""
        cycle = 2 * key - 2
        for i in range(key):
            for j in range(i, len(text), cycle):
                result += text[j]
                if i != 0 and i != key - 1:
                    k = j + cycle - 2 * i
                    if k < len(text):
                        result += text[k]
        return result

    return encrypt(text, key) if not decrypt else decrypt(text, key)
