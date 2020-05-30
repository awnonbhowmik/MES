from pylab import *
from matplotlib.pyplot import figure
figure(num=None, figsize=(8, 6), dpi=75, facecolor='w', edgecolor='k')
x = linspace(-2*pi, 2*pi)
plot(x, sin(x), label="sin x")
plot(x, cos(x), 'r-', label="cos x")
plot(x, -sin(x), 'g--', label="-sin x")
legend(loc="best")
show()