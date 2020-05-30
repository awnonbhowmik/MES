from Crypto.Cipher import AES
import time

t1 = time.time()
key = '0123456789abcdef'*2
IV = 16 * '\x00'           
mode = AES.MODE_CBC
encryptor = AES.new(key, mode, IV=IV)

text = 'abcdefghijklmnop'
ciphertext = encryptor.encrypt(text)
print(ciphertext)
decryptor = AES.new(key, mode, IV=IV)
plain = decryptor.decrypt(ciphertext)
print(time.time()-t1)