# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 17:54:47 2019

@author: Ebru
"""

import random

import math

def data(p,x,y):
    sehirler=[]
    with open("ch150.tsp") as b:
        locations = b.read()
        for location in locations.split("NODE_COORD_SECTION")[1:]:
            sehirler=(location.splitlines()[1:-1])
    p=[0]
    x=[]
    y=[]
    for i in sehirler:
        p.append(int(i.split(" ")[0]))
        x.append(float(i.split(" ")[1]))
        y.append(float(i.split(" ")[2]))
    return p[:-1],x,y

def simulatedAnnealing(p,x,y):
    mean=0;
    total=0;
    std=0;
    N = len(x)
    def objFunc(p):
        cost = 0
        for i in range(0,N-1):
            xd = x[p[i]] - x[p[i+1]]
            yd = y[p[i]] - y[p[i+1]]
            dxy = math.sqrt(xd * xd + yd *yd)
            cost = cost + dxy
        return cost
    
    E_best = objFunc(p)
    E_curr = objFunc(p)
    E_new = objFunc(p)
    
    print("First solution:",E_best)
    result = []
    T_start = 100000
    cooling_factor = 0.99
    T = T_start
    p_new = p.copy()
    p_curr = p.copy()
    iter = 0
    ITER_MAX=1000
    for i in range(0,ITER_MAX):
        while T > 0.001:
            
            swap1 = math.floor(random.uniform(0,1) * N)
            swap2 = math.floor(random.uniform(0,1) * N)
            while swap1 == swap2:
                swap2 = math.floor(random.uniform(0,1) * N)
            p_new = p_curr.copy()
            temp = p_new[swap1]
            p_new[swap1] = p_new[swap2]
            p_new[swap2] = temp
            E_new = objFunc(p_new)
            Delta_E = E_new - E_curr
            if Delta_E < 0:
                E_curr = E_new
                p_curr = p_new.copy()
                if E_curr < E_best:
                    E_best = E_curr 
            else:
                Prob = math.exp(-Delta_E/T)
                r = random.uniform(0,1)
                if r < Prob:
                    E_curr = E_new
                    p_curr = p_new.copy()
            T = T * cooling_factor
            iter = iter + 1
            mean=mean+E_curr
            result.append(E_curr)
   
    mean=mean/iter;
    # standart sapma
    for i in range(len(result)):
        total=total+(result[i]-mean)**2
    std=math.sqrt(total/(len(result)-1))
        
     
    print('E_best',E_best,'iter:',iter)
    print('Max',max(result))
    print('Min',min(result))
    print('Mean:',mean)
    print('Standart Sapma:',std)
            

x=[]
y=[]
p=[]
p,x,y=data(p,x,y)

simulatedAnnealing(p,x,y)