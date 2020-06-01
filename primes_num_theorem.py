from scipy import optimize
from sympy import *
import numpy as np
from matplotlib import pyplot as plt

def primesLessThan_N(n):
    p = 1
    while(prime(p)<n):
        p += 1
    return p-1

print('------------ #Primes < n ------------')

n = 1000

num_primes = []
for i in range(2,n+1):
    num_primes.append(primesLessThan_N(i))

x = np.arange(2,n+1)
y = num_primes

log_values = []
for i in x:
    log_values.append(i/np.log(i))

print(x)
print(y)
print(log_values)

def test_func(x, a, b):
    return x/np.log(x*a+b) 

param, param_cov = optimize.curve_fit(test_func, x, y)
print('Curve Parameter (a,b) = ',param)
ans = x/np.log(param[0]*x+param[1]) 
  

plt.plot(x, y,'-', color ='blue', label ="Actual") 
plt.plot(x, log_values, '-', color ='red', label ="x/ln(x)")
plt.plot(x, ans, '-', color ='green', label ="Optimized")
plt.xlabel('N')
plt.ylabel('#Primes')
plt.legend()
plt.show()
