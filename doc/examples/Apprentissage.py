# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

    toto = genfromtxt('Apprentissage.mat')
    tata = genfromtxt('Appris.mat')
    plot(toto[:,0],toto[:,1])
    plot(range(1,121,10),tata)
    mean(toto[:,1]),mean(tata)

