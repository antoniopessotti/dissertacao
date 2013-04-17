#-*- coding: utf8 -*-
import numpy as n, scikits.audiolab as a

# Peça musical baseada em sons estáticos
# são mixagens de sons básicos apresentados na sessão 2.1

f_a=44100 # 44.1kHz, frequência de amostragem de CDs
Delta=30. # cada quadro terá 30 segundos
Lambda=Delta*f_a # numero de amostras

ii=n.linspace(0,Delta*2*n.pi,Lambda,endpoint=False)

# frequencias que dividem f_a
fs=[]
for i in xrange(1,f_a/2+1):
    if f_a/float(i)==int(f_a/i):
        fs.append(i)

### Quadro 1: senoides no grave em batimento e no agudo uma
# dente de serra bem suave

f1=100
f2=100.5

som=n.sin(ii*f1)+n.sin(ii*f2)
dente_aguda=(n.arange(Lambda)%4-2)
som+=dente_aguda/80

# normalizando no intervalo [-1,1]
som=((som -som.min())/(som.max()-som.min()))*2-1

a.wavwrite(som,"quadro1.wav",f_a)


### Quadro 2: 3 conjuntos separados de triangulares

fs2=fs[20:21]+fs[65:70]+fs[77:]
#fs2=[25, 28, 30, 35, 36, 1764, 2100, 2205, 2450, 2940, 11025, 14700, 22050]

som=n.zeros(Lambda)
ii=n.arange(Lambda)
for f in fs2:
    lambda_f=f_a/f
    som+=(1-n.abs(2-(4./lambda_f)*(ii%lambda_f)))*(1./f**1.2)

# normalizando no intervalo [-1,1]
som=((som -som.min())/(som.max()-som.min()))*2-1

a.wavwrite(som,"quadro2.wav",f_a)


### Quadro 3: estereofonia alternada no espectro harmônico
f=50.
fs3=[f*i for i in xrange(1,7)] # 6 harmonicos
som_d=n.zeros(Lambda)
som_e=n.zeros(Lambda)
ii=n.linspace(0,Delta*2*n.pi,Lambda,endpoint=False)
i=0
for f in fs3:
    if i%2 == 0:
        som_d+=n.sin(f*ii)*(1./f)
    else:
        som_e+=n.sin(f*ii)*(1./f)
    i+=1
som=n.vstack((som_d,som_e)).T
 
som=((som -som.min())/(som.max()-som.min()))*2-1

a.wavwrite(som,"quadro3.wav",f_a)


### Quadro 4: batimentos intercalados por ouvido e com defasagens

fs4=n.array([50,51.01,52.01,53])
som_d=n.zeros(Lambda)
som_e=n.zeros(Lambda)
ii=n.linspace(0,Delta*2*n.pi,Lambda,endpoint=False)
i=0
for f in fs4:
    if i%2 == 0:
        som_d+=n.sin(f*ii)*(1./f)
    else:
        som_e+=n.sin(f*ii)*(1./f)
    i+=1
som=n.vstack((som_d,som_e)).T

fs4=n.array([500,501.01,502.01,503])
som_d=n.zeros(Lambda)
som_e=n.zeros(Lambda)
ii=n.linspace(0,Delta*2*n.pi,Lambda,endpoint=False)
i=0
for f in fs4:
    if i%2 == 0:
        som_d+=n.sin(f*ii)*(1./f)
    else:
        som_e+=n.sin(f*ii)*(1./f)
    i+=1
som+=n.vstack((som_d,som_e)).T/60

 
som=((som -som.min())/(som.max()-som.min()))*2-1

a.wavwrite(som,"quadro4.wav",f_a)


# Quadro 5: Dente de serra grave bate com harmonico em cada lado

f=42. # Hz, freq da dente
lambda_f=44100/f
dente=((n.arange(float(Lambda))%lambda_f)/lambda_f)*2-1

ii=n.linspace(0,Delta*2*n.pi,Lambda,endpoint=False)
som=dente+n.sin(ii*43)+n.sin(ii*84) + n.sin(ii*126.3)

som=((som -som.min())/(som.max()-som.min()))*2-1

a.wavwrite(som,"quadro5.wav",f_a)





