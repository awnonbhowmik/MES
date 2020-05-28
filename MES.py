import numpy as np
from sympy import prime
from sympy.ntheory.modular import crt
import random
import time

def cantor_pair(k1, k2, safe=True):
    z = int(0.5 * (k1 + k2) * (k1 + k2 + 1) + k2)
    if safe and (k1, k2) != cantor_unpair(z):
        raise ValueError("{} and {} cannot be paired".format(k1, k2))
    return z

def cantor_unpair(z):
    w = np.floor((np.sqrt(8 * z + 1) - 1) / 2)
    t = (w**2 + w) / 2
    y = int(z - t)
    x = int(w - y)
    # assert z != pair(x, y, safe=False):
    return (x, y)

def padding(plain_text,block_size):
    plain_text += '0'*(block_size-len(plain_text))
    return plain_text

def chunkstring(string, length):
    return list(string[0+i:length+i] for i in range(0, len(string), length))

def reduced_ascii_chunks(ascii_chunks):
    cantor_reduced_list = []
    for i in range(0,len(ascii_chunks)-1,2):
        cantor_reduced_list.append(cantor_pair(ascii_chunks[i],ascii_chunks[i+1]))
    return cantor_reduced_list

def encrypt_decrypt(plain_text,block_size):
    t1 = time.time()
    n = len(plain_text)
    
    plain_text_chunks = []
    if n < block_size:
        plain_text_chunks.append(padding(plain_text,block_size))
    else:
        chunks = chunkstring(plain_text,block_size)
        for i in range(len(chunks)):
            plain_text_chunks.append(padding(chunks[i],block_size))

    ascii_chunks = []
    for chunk in plain_text_chunks:
        t = []
        for i in chunk:
            t.append(ord(i))
        ascii_chunks.append(t)

    cantor_reduced_list = []
    for chunk in ascii_chunks:
        cantor_reduced_list.append(reduced_ascii_chunks(chunk))

    temp = []
    for chunk in cantor_reduced_list:
        for i in chunk:
            temp.append(i)
    lower_index = max(temp)

    M = []
    for i in range(block_size//2):
        x = prime(random.randint(lower_index,lower_index+1000))
        if x not in M:
            M.append(x)

    # print('Private key generated : ',end='')
    # print(M)

    # Applying the Chinese Remainder Theorem to get X

    cipher_text = []
    for chunk in cantor_reduced_list:
        x = crt(M,chunk)
        cipher_text.append(round(x[0]))
    # print('Encrypted Cipher Text : ',cipher_text)


    # ---------------------------------DECRYPTION-----------------------------------
    # private_key - known
    # cipher_text - known
    # block_size  - known


    dec_M = M

    dec_cantor_reduced_list = []
    for x in cipher_text:
        t = []
        for mi in dec_M:
            t.append(x%mi)
        dec_cantor_reduced_list.append(t)
    # print(dec_cantor_reduced_list)

    decrypted_ascii_list = []
    for chunk in dec_cantor_reduced_list:
        t = []
        for i in range(len(chunk)):
            x,y = cantor_unpair(chunk[i])
            t.append(x)
            t.append(y)
        decrypted_ascii_list.append(t)
    
    decrypted_text_list = []
    for chunk in decrypted_ascii_list:
        for i in chunk:
            if chr(i)!='0':
                decrypted_text_list.append(chr(i))
    # print('Decrypted Text : ',end='')
    # print(''.join(map(lambda x:str(x),decrypted_text_list)))
    print('Operation Runtime : {} seconds'.format(time.time()-t1))
