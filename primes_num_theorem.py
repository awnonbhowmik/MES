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

n = 100

num_primes = []
for i in range(2,n+1):
    num_primes.append(primesLessThan_N(i))

x = np.arange(2,n+1)

log_values = []
for i in x:
    log_values.append(i/np.log(i))


def test_func_num_primes(x, a, b):
    return x/np.log(x*a+b) 

param, param_cov = optimize.curve_fit(test_func_num_primes, x, num_primes)
# print('Curve Parameter (a,b) = ',param)
ans = x/np.log(param[0]*x+param[1]) 

fig = plt.figure(figsize=(8, 6))
plt.subplot(2,1,1)
plt.plot(x, num_primes,'-', color ='blue', label ="Actual #Primes") 
plt.plot(x, log_values, '-', color ='red', label ="N/ln(N)")
plt.plot(x, ans, '-', color ='green', label ="Optimized")
plt.title('Number of Primes')
plt.xlabel('N')
plt.ylabel('#Primes')
plt.legend(loc="best")

prime_density = []
for i in range(0,len(num_primes)):
    prime_density.append(num_primes[i]/x[i])

density_log_values = []
for i in x:
    density_log_values.append(1/np.log(i))

def test_func_prime_density(x, a, b):
    return 1/np.log(x*a+b) 

param, param_cov = optimize.curve_fit(test_func_prime_density, x, prime_density)
# print('Curve Parameter (a,b) = ',param)
ans = 1/np.log(param[0]*x+param[1]) 


plt.subplot(2,1,2)
plt.plot(x, prime_density,'-', color ='blue', label ="Actual Density") 
plt.plot(x, density_log_values, '-', color ='red', label ="1/ln(N)")
plt.plot(x, ans, '-', color ='green', label ="Optimized")
plt.title('Prime Density')
plt.xlabel('N')
plt.ylabel('Density')
plt.legend(loc="best")

plt.tight_layout()
plt.show()
