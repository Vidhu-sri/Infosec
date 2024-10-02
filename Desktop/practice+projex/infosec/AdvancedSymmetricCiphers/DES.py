import enum

from constants import CP_1, CP_2, PI, PI_1, S_BOX, SHIFT, E, P


__all__ : tuple[str,...] = ("_des_encryption",)

def string_to_bitarray(text:str) -> list:
    array = []
    for char in text:
        array.extend([int(i) for i in list(binvalue(char,8))])
    return array

    
def binvalue(val: int,bitsize: int) -> str:
    binval = bin(val)[2:] if isinstance(val,int) else bin(ord(val))[2:]
    assert len(binval) <= bitsize, "binary value larges than bitsize"
    binval = '0'*(bitsize-len(binval)) + binval
    return binval

def bitarray_to_string(bitarray:list):  #reconstruct string from bitarray
    return ''.join([chr(int(y,2)) for y in [''.join([str(i) for i in _byte])  for _byte in split_into_blocks(bitarray,8)]])

def split_into_blocks(bitarray:list[int], blocksize:int) -> list[list[int]]:
    return [bitarray[i:i+blocksize] for i in range(0,len(bitarray),blocksize)]

class Action(enum.Enum):
    ENCRYPT = enum.auto()
    DECRYPT = enum.auto()


class DES:
    def __init__(self):
        self.password = None
        self.text = None
        self.keys = list()

    def run(self, key:str, text: str, action:Action = Action.ENCRYPT,padding: bool = True):

        if len(key) < 8:
            raise "Key should be 8 bytes long"
        elif len(key) > 8:
            key = key[:8]
        
        self.password = key
        self.text = text

        if padding and action == Action.ENCRYPT:
            self.add_padding()
        elif len(self.text)%8:
            raise "Data size should be a  multiple of 8"

        self.generate_keys()
        text_blocks = split_into_blocks(self.text,8)
        result = []

        for block in text_blocks:
            block = string_to_bitarray(block)
            block = self.permut(block,PI)
            l,r = split_into_blocks(block,32)
            tmp = None

            '''
            L_n = R_n-1
            R_n = L_n-1 XOR f(R_n-1,Kn) #Kn is nth key
            f(R_n-1,K_n) = permut(SBox(E(R_n-1) XOR Kn ))
            E(R_n-1) to expan the right subblock to 48 bits (len(Kn))
            '''
            for i in range(16):  #the 16 rounds
                r_e = self.permut(r,E)  #match the 48 bit keysize
                
                if action == Action.ENCRYPT:
                    tmp = self.xor(self.keys[i],r_e)
                else:
                    tmp = self.xor(self.keys[15-i],r_e) #if decrypt start by the last key

                tmp = self.substitute(tmp)  #substitute using SBoxes
                tmp = self.permut(tmp,P) #permute by p table
                tmp = self.xor(l,tmp)
                l = r
                r = tmp
        result += self.permut(r+l,PI_1)  #the final permutation

        final_res = bitarray_to_string(result)

        if padding and action == Action.DECRYPT:
            return self.remove_padding(final_res)
        else:
            return final_res
        

    def substitute(self,d_e: list[int]) -> list[int]:
        subblocks = split_into_blocks(d_e,6)
        result = []

        for i  in range(len(subblocks)):
            block = subblocks[i]
            row = int(str(block[0])+str(block[5]),2)
            col = int("".join([str(x) for x in block[1:][:-1]]), 2)
            val = S_BOX[i][row][col]
            bin = binvalue(val,4)
            result += [int(x) for x in bin]
        return result

    def permut(self,block:list[int], table:list[int]) -> list[int]:
        return [block[x-1] for x in table]
    
    def xor(self,t1:list[int], t2: list[int]) -> list[int]:
        return [x^y for x,y in zip(t1,t2)]
    
    def generate_keys(self)->None:
        self.keys = []
        key = string_to_bitarray(self.password)
        key = self.permut(key,CP_1)
        c,d = split_into_blocks(key,28)

        for i in range(16):
            c,d = self.shift(c,d,SHIFT[i])
            tmp = c+d
            self.keys.append(self.permut(tmp,CP_2))
        
    def shift(self,g:list[int], d: list[int], n:int) -> tuple[list[int],list[int]]:
        return g[n:] + g[:n], d[n:] + d[:n] #rotation
     
    def add_padding(self) -> None:   #padding using PKCS5 spec.
        pad_len = 8 - (len(self.text)%8)
        self.text += pad_len*chr(pad_len)
    
    def remove_padding(self,data:str) -> str:
        pad_len = ord(data[-1])
        return data[:-pad_len]
    
    def encrypt(self,key: str, text: str, padding: bool = True) -> str:
        return self.run(key,text,Action.ENCRYPT,padding)

    def decrypt(self,key:str,text:str,padding:bool=True) ->str:
        return self.run(key,text, Action.DECRYPT,padding)

def _des_encryption(text:str,key:int, decrypt: bool = False) -> str:
    return DES().decrypt(key,text) if decrypt else DES().encrypt(key,text)


print(_des_encryption("hello", "0E329232"))

