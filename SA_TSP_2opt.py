# -*- coding: utf-8 -*-
"""
Created on Fri Nov  8 17:31:29 2019

@author: Ebru
"""
import random
import math
def data_read(p,X,Y): #verileri p,x,y olarak ayır
    veriler=[]
    with open("ch150.tsp") as b:
        data = b.read()
        for d in data.split("NODE_COORD_SECTION")[1:]:
            veriler=(d.splitlines()[1:-1])
    p=[0]
    X=[]
    Y=[]
    for i in veriler:
        p.append(int(i.split(" ")[0]))
        X.append(float(i.split(" ")[1]))
        Y.append(float(i.split(" ")[2]))
    return p[:-1],X,Y

def objFunc(p):
    N = len(x)
    cost = 0
    for i in range(0,N-1):
        xd = x[p[i]] - x[p[i+1]]
        yd = y[p[i]] - y[p[i+1]]
        dxy = math.sqrt(xd * xd + yd *yd)
        cost = cost + dxy
    return cost

#random alınan noktaların bağlantıları değiştirilir
def  swap_2opt ( route, node1 , node2 ):
    tmp = route[node1:node2]
    tmp_state = route[:node1] + tmp[::-1] +route[node2:]       
    return tmp_state  

def simulatedAnnealing(p,x,y,ITER_MAX):
    mean=0
    total=0
    std=0
    
    N=len(x)
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
    for i in range(ITER_MAX):
        while T > 0.001:
            swap1 = math.floor(random.uniform(0,1) * N)
            swap2 = math.floor(random.uniform(0,1) * N)
            #random noktalar
            while swap1 == swap2:
                swap2 = math.floor(random.uniform(0,1) * N)
            # random alınan değerler swap_2opt fonksiyonuna gönderilir
            p_new=swap_2opt(p_curr,swap1,swap2)
            # geri dönen yeni turun maliyeti hesaplanır
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
            result.append(E_curr)
            mean=mean+E_curr
            iter = iter + 1
    #        
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
p,x,y=data_read(p,x,y)
simulatedAnnealing(p,x,y,1000)

