import scipy as sp
import matplotlib.pyplot as plt


def error(f,x,y):
	return sp.sum((f(x)-y)**2)


data = sp.genfromtxt("web_traffic.tsv", delimiter="\t")
print(data[:10])

x = data[:,0]
y = data[:,1]
x = x[~sp.isnan(y)]
y = y[~sp.isnan(y)]


fp1, residuals, rank, sv, rcond = sp.polyfit(x,y,1, full=True)
print("Model parameters: %s" % fp1)
f1 = sp.poly1d(fp1)
print(error(f1,x,y))
fx = sp.linspace(0,x[-1],1000) #generate x-values for plotting


f2p = sp.polyfit(x, y, 2)
print(f2p)
f2 = sp.poly1d(f2p)
print(error(f2, x, y))


plt.scatter(x,y,s=10)
plt.title("Web traffic over the last month")
plt.xlabel("Time")
plt.ylabel("Hits/hour")
plt.xticks([w*7*24 for w in range(10)],['week %i' % w for w in range(10)])
plt.plot(fx,f1(fx), linewidth=4)
plt.plot(fx,f2(fx), linewidth=2)
plt.legend(["d=%i" m.order for m in models],loc="upper left")
plt.autoscale(tight=True)
plt.grid(True, linestyle='-',color='0.75')
plt.show()
