import numpy as np
import string


def make_matrix(plaintext,key_matrix):

    m = len(key_matrix)
    plaintext = plaintext.upper().replace(' ','')
    plaintext = [ord(char) - ord('A') for char in plaintext]
    plaintext.extend([0 for _ in range(len(plaintext)%m)])
    matrix = []
    for i in range(0,len(plaintext),m):
        matrix.append(plaintext[i:i+m])
    return matrix

key_matrix = [[3, 3], [2, 7]]
plaintext = "WE"
plaintext = np.array(make_matrix(plaintext,key_matrix))
key_matrix = np.array(key_matrix)
ciphertext = map(lambda x: [string.ascii_uppercase[i] for i in x], np.dot(key_matrix, plaintext.T) % 26)



print(list(ciphertext))

