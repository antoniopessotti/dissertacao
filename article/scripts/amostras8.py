#-*- coding: utf-8 -*-
# http://matplotlib.sourceforge.net/examples/api/legend_demo.html
# 
import pylab as p, numpy as n, scikits.audiolab as a
f=n.fft.fft

#n8=n.random.rand(8)*2-1
n8=n.array([-0.22746437,  0.4079638 ,  0.8548025 , -0.19153126,  0.68216695,0.45399424, -0.81023872, -0.85826893])
#n4=n.array([ 0.58003705, -0.30828309, -0.29797696, -0.99219078])
p.plot(n8,"bo")

ff=f(n8)

# Primeiro componente, 0Hz
a0=n.real(ff[0]) 
b0=n.imag(ff[0]) # sempre zero

# Segundo componente, t_a/N Hz
ab1=n.abs(ff[1]) # (a**2+b**2)**0.5
a1=n.real(ff[1])
b1=n.imag(ff[1])
fas=n.arctan(b1/a1) # fase fas=n.angle(f[1])
if a1<0: fas+=n.pi # segundo e terceiro quadrantes somam pi
print("abs: %s, a1: %s, b1: %s, fas: %s" % (ab1,a1,b1,fas))

# Segundo componente, t_a/N Hz
ab2=n.abs(ff[2]) # (a**2+b**2)**0.5
a2=n.real(ff[2])
b2=n.imag(ff[2])
fas2=n.arctan(b2/a2) # fase fas=n.angle(f[1])
if a2<0: fas2+=n.pi # segundo e terceiro quadrantes somam pi
print("abs: %s, a2: %s, b2: %s, fas2: %s" % (ab2,a2,b2,fas2))

# Segundo componente, t_a/N Hz
ab3=n.abs(ff[3]) # (a**2+b**2)**0.5
a3=n.real(ff[3])
b3=n.imag(ff[3])
fas3=n.arctan(b3/a3) # fase fas=n.angle(f[1])
if a3<0: fas3+=n.pi # segundo e terceiro quadrantes somam pi
print("abs: %s, a3: %s, b3: %s, fas3: %s" % (ab3,a3,b3,fas3))

ab4=n.abs(ff[4]) # (a**2+b**2)**0.5
a4=n.real(ff[4])
b4=n.imag(ff[4])
fas4=n.arctan(b4/a4) # fase fas=n.angle(f[1])
if a4<0: fas4+=n.pi # segundo e terceiro quadrantes somam pi
print("abs: %s, a4: %s, b4: %s, fas4: %s" % (ab4,a4,b4,fas4))




fr1=(2*n.pi/8)/2 #ciclo em 8 * \delta_a, metade do intervalo angular 
fr2=1/2. # metade de \delta_a
#fr1=fr2=0
ii=n.linspace(0-fr1,2*n.pi-fr1,200, endpoint=False) # [0,2*pi] ciclo completo
iii=n.linspace(0-fr2,8-fr2,200, endpoint=False) # [0,3] == 3 \delta_a, período

s=(1/8.)*a4*n.cos(4*ii)+(2/8.)*ab3*n.cos(3*ii+fas3)+   (2/8.)*ab2*n.cos(2*ii+fas2)+(2/8.)*ab1*n.cos(ii+fas)+a0/8
p.plot(iii,s,"m", linewidth=3, label=r"$\oplus$")
ss=(1/8.)*ab1*n.cos(ii+fas)
sss=(2/8.)*ab2*n.cos(2*ii+fas2)
ssss=(2/8.)*ab3*n.cos(3*ii+fas3)
sssss=(1/8.)*ab4*n.cos(4*ii+fas4)
p.plot(iii,[a0/8]*200,"k:", label=r"$\frac{a_0}{8}$")
p.plot(iii,ss,"r-.", label=r"$\frac{2}{8}\sqrt{a_1^2+b_1^2}cos\left(\frac{2\pi . 1 }{8}i + tg^{-1}\left(\frac{b_1}{a_1}\right)\right)$")
p.plot(iii,sss,"g--",label=r"$\frac{2}{8}\sqrt{a_2^2+b_2^2}cos\left(\frac{2\pi . 2 }{8}i + tg^{-1}\left(\frac{b_2}{a_2}\right)\right)$")
p.plot(iii,ssss,"c",label=r"$\frac{2}{8}\sqrt{a_3^2+b_3^2}cos\left(\frac{2\pi . 3 }{8}i + tg^{-1}\left(\frac{b_3}{a_3}\right)\right)$")
p.plot(iii,sssss,"y",label=r"$\frac{a_4}{8}cos\left(\frac{2\pi . 4 }{8}i \right)$")
#p.plot(iii,ss,"r--", label=r"$\frac{1}{4}\sqrt{a_2^2 + b_2^2}cos\left(\frac{2\pi . 2 }{\Lambda}i - tg^{-1}\left(\frac{b_2}{a_2}\right)\right)$")

p.legend(loc="upper right")

p.xlim(-1.2,8.2)
p.ylim(-1.1,1.1)

p.xticks((-1,0,1,2,3,4),(r"$-\delta_a$",r"$0$",r"$\delta_a$",r"$2\delta_a$",r"$3\delta_a$",r"$4\delta_a$"))

p.ylabel(r"amplitude $\rightarrow$")
p.xlabel(r"time $\rightarrow$")
p.show()
