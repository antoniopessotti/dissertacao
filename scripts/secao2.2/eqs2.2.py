#-*- coding: utf8 -*-
import numpy as n, scikits.audiolab as a

f_a = 44100 # Hz, frequência de amostragem

############## 2.2.1 Tabela de busca (LUT)
# tamanho da tabela: use par para não conflitar abaixo
# e ao menos 1024
Lambda_tilde=Lt=1024

# Senoide
foo=n.linspace(0,2*n.pi,Lt,endpoint=False)
S_i=n.sin(foo) # um período da senoide com T amostras

# Quadrada:
Q_i=n.hstack(  ( n.ones(Lt/2)*-1 , n.ones(Lt/2) )  )

# Triangular:
foo=n.linspace(-1,1,Lt/2,endpoint=False)
Tr_i=n.hstack(  ( foo , foo*-1 )   )

# Dente de Serra:
D_i=n.linspace(-1,1,Lt)

# som real, importar período e
# usar T correto: o número de amostras do período

f=110. # Hz
Delta=3.4 # segundos
Lambda=int(Delta*f_a)

# Amostras:
ii=n.arange(Lambda)

### 2.30
Gamma_i=n.array(ii*f*Lt/f_a,dtype=n.int)
L_i=Tr_i # podemos usar igualmente S_i, Q_i, D_i ou qualquer período de som real suficientemente grande
TfD_i=L_i[Gamma_i%Lt]


############## 2.2.2 Variações incrementais de frequência e amplitude
# VARIAÇÕES DE FREQUÊNCIA
f_0=100. # freq inicial em Hz
f_f=300. # frq final em Hz
Delta=2.4 # duração

Lambda=int(f_a*Delta)
ii=n.arange(Lambda)
### 2.31 - variação linear
f_i=f_0+(f_f-f_0)*ii/(float(Lambda)-1)
### 2.32
D_gamma_i=f_i*Lt/f_a
Gamma_i=n.cumsum(D_gamma_i)
Gamma_i=n.array(Gamma_i,dtype=n.int)
### 2.33
Tf0ff_i=L_i[Gamma_i%Lt]

### 2.34 - variação exponencial
f_i=f_0*(f_f/f_0)**(ii/(float(Lambda)-1))
### 2.35
D_gamma_i=f_i*Lt/f_a
Gamma_i=n.cumsum(D_gamma_i)
Gamma_i=n.array(Gamma_i,dtype=n.int)
### 2.36
Tf0ff_i=L_i[Gamma_i%Lt]


# VARIAÇÕES DE AMPLITUDE
# sintetizando um som qualquer para realizamos a variação de amplitude
f=220. # Hz
Delta=3.9 # segundos
Lambda=int(Delta*f_a)

# Amostras:
ii=n.arange(Lambda)

# (como em 2.30)
Gamma_i=n.array(ii*f*Lt/f_a,dtype=n.int)
L_i=Tr_i # podemos usar igualmente S_i, Q_i, D_i ou qualquer período de som real suficientemente grande
T_i=TfD_i=L_i[Gamma_i%Lt]

a_0=1. # razão da amplitude em que iniciamos
a_f=12. # razão da amplitude em que finalizamos
alpha=1. # índice de suavidade da transição
### 2.37
A_i=a_0*(a_f/a_0)**((ii/float(Lambda))**alpha)
### 2.38
T2_i=A_i*T_i

### 2.39
A_i=a_0+(a_f-a_0)*(ii/float(Lambda))

### 2.40
V_dB=31. # transição em decibels
T2_i=T_i*((10*(V_dB/20.))**(  (ii/float(Lambda))**alpha  ))



############## 2.2.3 Aplicação de filtros digitais
# VEJA iir.py para a geraçào da figura 2.17
# T_i herdado
# resposta ao impulso sintética (reverb)
H_i=(n.random.random(10)*2-1)*n.e**(-n.arange(10))

### 2.41
T2_i=n.convolve(T_i,H_i)

### 2.42 veja as proximas linhas :-)
fc=.1
### 2.43 passa baixas de polo simples
x=n.e**(-2*n.pi*fc) # fc=> freq de corte em 3dB
# coeficientes
a0=1-x
b1=x
# aplicando o filtro
T2_i=[T_i[0]]
for t_i in T_i[1:]:
    T2_i.append(t_i*a_0+T2_i[-1]*b1)

### 2.44 passa altas de polo simples
x=n.e**(-2*n.pi*fc) # fc=> freq de corte em 3dB
a0=(1+x)/2
a1=-(1+x)/2
b1=x

# aplicando o filtro
T2_i=[a0*T_i[0]]
last=T_i[0]
for t_i in T_i[1:]:
    T2_i+=[  a0*t_i + a1*last + b1*T2_i[-1]  ]
    last=n.copy(t_i)


### 2.45 Variáveis auxiliares para os filtros nó
fc=.1
bw=.05

### 2.46 passa banda
r=1-3*bw
k=(1-2*r*n.cos(2*n.pi*fc)+r**2)/(2-2*n.cos(2*n.pi*fc))

# coefs passa banda
a0=1-k
a1=-2*(k-r)*n.cos(2*n.pi*fc)
a2=r**2 -k
b1=2*r*n.cos(2*n.pi*fc)
b2=-r**2

# aplicacao do filtro em T_i resultando em T2_i
T2_i=[a0*T_i[0]]
T2_i+=[a0*T_i[1]+a1*T_i[0]+b1*T2_i[-1]]
last1=T_i[1]
last2=T_i[0]
for t_i in T_i[2:]:
    T2_i+=[a0*t_i+a1*last1+a2*last2+b1*T2_i[-1]+b2*T2_i[-2]]
    last2=n.copy(last1)
    last1=n.copy(t_i)

### 2.47 rejeita banda
a0=k
a1=-2*k*n.cos(2*n.pi*fc)
a2=k
b1=2*r*n.cos(2*n.pi*fc)
b2=-r**2

# aplicacao do filtro em T_i resultando em T2_i
T2_i=[a0*T_i[0]]
T2_i+=[a0*T_i[1]+a1*T_i[0]+b1*T2_i[-1]]
last1=T_i[1]
last2=T_i[0]
for t_i in T_i[2:]:
    T2_i+=[a0*t_i+a1*last1+a2*last2+b1*T2_i[-1]+b2*T2_i[-2]]
    last2=n.copy(last1)
    last1=n.copy(t_i)


############## 2.2.4 Ruídos
# VEJA ruidos.py para o script que gerou a figura 2.18
Lambda = 100000 # Lambda sempre par
# diferença das frequências entre coeficiêntes vizinhos:
df=f_a/float(Lambda)

### 2.48 Ruido branco
# geracao de espectro com modulo 1 uniforme
# e fase aleatoria
coefs=n.exp(1j*n.random.uniform(0, 2*n.pi, Lambda))
# real par, imaginaria impar
coefs[Lambda/2+1:]=n.real(coefs[1:Lambda/2])[::-1] - 1j*n.imag(coefs[1:Lambda/2])[::-1]
coefs[0]=0. # sem bias
coefs[Lambda/2]=1. # freq max eh real simplesmente

# as frequências relativas a cada coeficiente
# acima de Lambda/2 nao vale
fi=n.arange(coefs.shape[0])*df 
f0=15. # iniciamos o ruido em 15 Hz
i0=n.floor(f0/df) # primeiro coeff a valer
coefs[:i0]=n.zeros(i0)
f0=fi[i0]

# realizando o ruído em suas amostras temporais
ruido=n.fft.ifft(coefs)
r=n.real(ruido)
r=((r-r.min())/(r.max()-r.min()))*2-1
a.wavwrite(r,'branco.wav',f_a)


### 2.49 Ruído rosa
# a cada oitava, perdemos 3dB
fator=10.**(-3/20.)
alphai=fator**(n.log2(fi[i0:]/f0))

c=n.copy(coefs)
c[i0:]=coefs[i0:]*alphai
# real par, imaginaria impar
c[Lambda/2+1:]=n.real(c[1:Lambda/2])[::-1] - 1j*n.imag(c[1:Lambda/2])[::-1]

ruido=n.fft.ifft(c)
r=n.real(ruido)
r=((r-r.min())/(r.max()-r.min()))*2-1
a.wavwrite(r,'rosa.wav',f_a)


### 2.50 Ruído marrom
# para cada oitava, perdemos 3dB
fator=10.**(-6/20.)
alphai=fator**(n.log2(fi[i0:]/f0))
c=n.copy(coefs)
c[i0:]=c[i0:]*alphai

# real par, imaginaria impar
c[Lambda/2+1:]=n.real(c[1:Lambda/2])[::-1] - 1j*n.imag(c[1:Lambda/2])[::-1]

# realizando amostras temporais do ruído marrom
ruido=n.fft.ifft(c)
r=n.real(ruido)
r=((r-r.min())/(r.max()-r.min()))*2-1
a.wavwrite(r,'marrom.wav',f_a)


### 2.51 Ruído azul
# para cada oitava, ganhamos 3dB
fator=10.**(3/20.)
alphai=fator**(n.log2(fi[i0:]/f0))
c=n.copy(coefs)
c[i0:]=c[i0:]*alphai

# real par, imaginaria impar
c[Lambda/2+1:]=n.real(c[1:Lambda/2])[::-1] - 1j*n.imag(c[1:Lambda/2])[::-1]

# realizando amostras temporais do ruído azul
ruido=n.fft.ifft(c)
r=n.real(ruido)
r=((r-r.min())/(r.max()-r.min()))*2-1
a.wavwrite(r,'azul.wav',f_a)


### 2.52 Ruido violeta
# a cada oitava, ganhamos 6dB
fator=10.**(6/20.)
alphai=fator**(n.log2(fi[i0:]/f0))
c=n.copy(coefs)
c[i0:]=c[i0:]*alphai

# real par, imaginaria impar
c[Lambda/2+1:]=n.real(c[1:Lambda/2])[::-1] - 1j*n.imag(c[1:Lambda/2])[::-1]

ruido=n.fft.ifft(c)
r=n.real(ruido)
r=((r-r.min())/(r.max()-r.min()))*2-1
a.wavwrite(r,'violeta.wav',f_a)

# 2.53 Ruído preto
# a cada oitava, perdemos mais que 6dB
fator=10.**(-12/20.)
alphai=fator**(n.log2(fi[i0:]/f0))
c=n.copy(coefs)
c[i0:]=c[i0:]*alphai

# real par, imaginaria impar
c[Lambda/2+1:]=n.real(c[1:Lambda/2])[::-1] - 1j*n.imag(c[1:Lambda/2])[::-1]

ruido=n.fft.ifft(c)
r=n.real(ruido)
r=((r-r.min())/(r.max()-r.min()))*2-1
a.wavwrite(r,'preto.wav',f_a)


############## 2.2.5 Usos musicais parte 1: trêmolo e vibrato, AM e FM
# VEJA: vibrato.py e tremolo.py para as figuras 2.19 e 2.20
f=220.
Lv=2048 # tamanho da tabela do vibrato
fv=1.5 # frequência do vibrato
nu=1.6 # desvio maximo em semitons do vibrato (profundidade)
Delta=5.2 # duração do som
Lambda=int(Delta*f_a)

# tabela do vibrato
x=n.linspace(0,2*n.pi,Lv,endpoint=False)
tabv=n.sin(x) # o vibrato será senoidal

ii=n.arange(Lambda) # índices
### 2.54 índices da tabela do vibrato
Gammav_i=n.array(ii*fv*float(Lv)/f_a, n.int) # índices para a LUT
### 2.55 padrão de oscilação do vibrato
Tv_i=tabv[Gammav_i%Lv] # padrão de variação do vibrato para cada amostra
### 2.56 frequências em cada amostra
F_i=f*(   2.**(  Tv_i*nu/12.  )   ) # frequência em Hz em cada amostra
### 2.57 índices para busca na tabela do som
D_gamma_i=F_i*(Lt/float(f_a)) # a movimentação na tabela por amostra
Gamma_i=n.cumsum(D_gamma_i) # a movimentação na tabela total
Gamma_i=n.array( Gamma_i, dtype=n.int) # já os índices
### 2.58 som em si
T_i=Tr_i[Gamma_i%Lt] # busca dos índices na tabela

a.wavwrite(T_i,"vibrato.wav",f_a) # escrita do som


### 2.59
Tt_i=n.copy(Tv_i)
V_dB=12. # decibels envolvidos na variação
A_i=10**((V_dB/20)*Tt_i)
### 2.60
Gamma_i=n.array(ii*f*Lt/f_a,dtype=n.int)
T_i=Tr_i[Gamma_i%Lt]*A_i
a.wavwrite(T_i,"tremolo.wav",f_a) # escrita do som


### 2.61 - Espectro da FM, implementada em 2.64-68
### 2.62 - Função de Bessel, foge ao escopo
### 2.63 - Espectro da AM, implementada em 2.69,70 abaixo

### 2.64 e 2.65
fv=60. # > 20Hz
Gammav_i=n.array(ii*fv*float(Lv)/f_a, n.int) # índices para a LUT
Tfm_i=tabv[Gammav_i%Lv] # padrão de variação do vibrato para cada amostra
### 2.66
f=330.
mu=40.
f_i=f+Tfm_i*mu
### 2.67
D_gamma_i=f_i*(Lt/float(f_a)) # a movimentação na tabela por amostra
Gamma_i=n.cumsum(D_gamma_i) # a movimentação na tabela total
Gamma_i=n.array( Gamma_i, dtype=n.int) # já os índices
### 2.68 FM
T_i=S_i[Gamma_i%Lt] # busca dos índices na tabela

a.wavwrite(T_i,"fm.wav",f_a) # escrita do som


### 2.69
Tam_i=n.copy(Tfm_i)
V_dB=12.
alpha=10**(V_dB/20.) # profundidade da AM
A_i=1+alpha*Tam_i
Gamma_i=n.array(ii*f*Lt/f_a,dtype=n.int)
### 2.70 AM
T_i=Tr_i[Gamma_i%Lt]*(A_i)
a.wavwrite(T_i,"am.wav",f_a) # escrita do som


############## 2.2.5 Usos musicais parte 2
### 2.71 Na peça Tremolos, Vibratos e a Frequência
### 2.72 ADSR
Delta=5. # duração total em segundos
Delta_A=0.1 # Ataque
Delta_D=.3 # Decay
Delta_R=.2 # Release
a_S=.1 # nível de sustentação

xi=1e-2 # -180dB para iniciar o fade in e finalizar o fade out
Lambda=int(f_a*Delta)
Lambda_A=int(f_a*Delta_A)
Lambda_D=int(f_a*Delta_D)
Lambda_R=int(f_a*Delta_R)

# Realização da envoltória ADSR: A_i
ii=n.arange(Lambda_A,dtype=n.float)
A=ii/(Lambda_A-1)
A_i=A
ii=n.arange(Lambda_A,Lambda_D+Lambda_A,dtype=n.float)
D=1-(1-a_S)*(   ( ii-Lambda_A )/( Lambda_D-1) )
A_i=n.hstack(  (A_i, D  )   )
S=a_S*n.ones(Lambda-Lambda_R-(Lambda_A+Lambda_D),dtype=n.float)
A_i=n.hstack( ( A_i, S )  )
ii=n.arange(Lambda-Lambda_R,Lambda,dtype=n.float)
R=a_S-a_S*((ii-(Lambda-Lambda_R))/(Lambda_R-1))
A_i=n.hstack(  (A_i,R)  )

# Realização do som
ii=n.arange(Lambda,dtype=n.float)
Gamma_i=n.array(ii*f*Lt/f_a,dtype=n.int)
### 2.70 AM
T_i=Tr_i[Gamma_i%Lt]*(A_i)

a.wavwrite(T_i,"adsr.wav",f_a) # escrita do som











