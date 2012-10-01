#-*- coding: utf8 -*-
import numpy as n, pylab as p

ax=p.subplot(111)
ax.annotate(r"$t_{12}'=\sum_{j=0}^9 \, h_j.t_{12-j}$", xy=(12.2, -2.65),  xycoords='data',
                xytext=(21, -3.95), textcoords='data',
                arrowprops=dict(facecolor='black', shrink=0.05),
                horizontalalignment='right', verticalalignment='top',
                )

ax.annotate(r"$t_{32}'=\sum_{j=0}^9 \, h_j.t_{32-j}$", xy=(31.8, -1.75),  xycoords='data',
                xytext=(30, -3.95), textcoords='data',
                arrowprops=dict(facecolor='black', shrink=0.05),
                horizontalalignment='right', verticalalignment='top',
                )





x=n.linspace(0,3*2*n.pi,50)
t=n.sin(x)
t=n.hstack((n.hstack((n.linspace(-1,1,16),n.linspace(-1,1,16))),n.linspace(-1,1,16)))
t*=.5

p.plot(t,'bo', label=r'trecho de sinal sonoro $\{t_i\}_0^{47}$')

#h=1./x[1:11]**.5
h=n.random.random(10)
h=n.array([ 0.5591728 ,  0.59152829,  0.43285462,  0.8870076 ,  0.44892785,0.33476906,  0.8808893 ,  0.39040725,  0.56887214,  0.54278373])
p.plot(range(3,13),h[::-1]+1,'ro',label=r'retrogrado da resposta ao impulso $\{h_{-i}\}_0^9$')
for i in xrange(3,12):
    p.plot([i,i],[-1,2],'y-.')
p.plot([12,12],[-5,2], 'y-.',linewidth=3)


p.plot(range(23,33),h[::-1]+1,'ro')
for i in xrange(23,32):
    p.plot([i,i],[-1,2],'y-.')
p.plot([32,32],[-5,2], 'y-.',linewidth=3)

c=n.convolve(t,h)
p.plot(c-2.5,'go', label=u'sinal convoluído ' + r'$\{(t*h)_i\}_0^{48+10-2=56}$')


#p.xlim(-1.2,4.2)
p.ylim(-7.2,2.5)

p.yticks((),())
p.xticks((),())
p.legend(loc="upper right")

p.show()
