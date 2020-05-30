from Crypto.Cipher import DES
import time
t1 = time.time()
des = DES.new('01234567', DES.MODE_ECB)
text = '0123456789abcdef'
cipher_text = des.encrypt(text)
cipher_text
des.decrypt(cipher_text)
print(time.time()-t1)