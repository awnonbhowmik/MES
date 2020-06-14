import streamlit as st
import numpy as np
import sympy
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


st.title('Modern Encryption Standard')
plain_text = st.text_input('Enter Plain Text: ')
n = len(plain_text)

block_size = st.slider('Block Size',4,256)

M = []
for i in range(1,block_size//2+1):
    M.append(sympy.ntheory.generate.nextprime(33024,ith=i))

random.shuffle(M)

priv_key = ''.join(str(M))
st.write('### Private key generated : ')
st.write(priv_key)

t1 = time.time()

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

# Applying the Chinese Remainder Theorem to get X
cipher_text = []
for chunk in cantor_reduced_list:
    x = crt(M,chunk)
    cipher_text.append(round(x[0]))
encr_txt = ''.join(str(cipher_text))
encr_txt = '\n'.join(encr_txt[i:i+72] for i in range(0, len(encr_txt), 72))
st.write('### Encrypted Cipher Text : ')
st.write(encr_txt)

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

dec_txt = ''.join(map(lambda x:str(x),decrypted_text_list))
st.write('### Decrypted Text : ')
st.write(dec_txt)
time_taken = '{} seconds'.format(time.time()-t1)
st.write('### Operation Runtime : ')
st.write(time_taken)
