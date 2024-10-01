

def generate_playfair_matrix(key):
    dim = 5
    key = sorted(list(set(key.upper().replace('J','I'))),key=lambda x: key.index(x))
    matrix = []
    matrix.extend(key+ [chr(i) for i in range(ord('A'), ord('Z')+1) if chr(i) not in key]) 
    matrix.remove('J')
    playfair_matrix = [matrix[dim*i:dim*(i+1)] for i in range(len(matrix)//dim)]
    return playfair_matrix



def find_position(char,matrix):
    for row in range(5):
        for col in range(5):
            if matrix[row][col] == char:
                return row,col
    return None,None

def prepare_text(plaintext):
    plaintext = plaintext.upper().replace("J","I").replace(" ","")
    prepared_text = ""
    i = 0
    while i<len(plaintext):
        if i == len(plaintext)-1:
            prepared_text+=plaintext[i]+'X'
            i+=1
        elif plaintext[i] == plaintext[i+1]:
            prepared_text += plaintext[i]+'X'
            i+=1
        else:
            prepared_text+= plaintext[i] + plaintext[i+1]
            i+=2
    return prepared_text


def playfair_encrypt(plaintext,matrix):

    plaintext = prepare_text(plaintext)
    ciphertext = ""

    for i in range(0,len(plaintext),2):
        row1,col1 = find_position(plaintext[i],matrix)
        row2,col2 = find_position(plaintext[i+1],matrix)

        if row1 == row2:
            ciphertext+= matrix[row1][(col1+1)%5] + matrix[row2][(col2+1)%5] 
            
        elif col1 == col2:
            ciphertext+= matrix[(row1+1)%5][col1] + matrix[(row2+1)%5][col2] 
            
        else:
            ciphertext+= matrix[row1][col2] + matrix[row2][col1]

    return ciphertext

# Example usage
key = "GUIDANCE"
plaintext = "The key is hidden under the door pad"
matrix = generate_playfair_matrix(key)
ciphertext = playfair_encrypt(plaintext, matrix)
print("Ciphertext:", ciphertext)


