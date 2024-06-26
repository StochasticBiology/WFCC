from random import seed, random
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
from bisect import bisect_left
seed(666)

def randcube(n,bias=0):
    graph = []
    for source in range(2**n):
        targets = set(range(n)) - set(i for i, digit in enumerate(reversed((bin(source)))) if digit == '1')
        randomlist = [random() for i in targets]
        weights = [float(k)/sum(randomlist) for k in randomlist]
        if bias == 1:
            weights.sort(reverse=True) 
        if bias == 2:
            weights.sort(reverse=False) 
        for i,t in enumerate(targets):
            graph.append((source,source+2**t,weights[i]))
    return graph

def null_cube(n):
    graph = []
    for source in range(2**n):
        targets = set(range(n)) - set(i for i, digit in enumerate(reversed((bin(source)))) if digit == '1')
        for t in targets:
            graph.append((source,source+2**t,1/len(targets)))
    return graph

def prob_to_flux(graph,already_sorted = True):
    if not already_sorted:
        graph = sorted(graph)
    nodeWeights, nodeInflux, newGraph = (dict(),dict(),list())
    node = graph[0][0]
    nodeWeights[node] = 1
    for edge in graph:
        if edge[0] != node:
            node = edge[0]
            nodeWeights = {node:nodeInflux[node]}
        flux = nodeWeights[node]*edge[2]
        newGraph.append((edge[0],edge[1],flux))
        if edge[1] not in nodeInflux.keys():
            nodeInflux[edge[1]] = flux
        else:
            nodeInflux[edge[1]] = nodeInflux[edge[1]] + flux
    return newGraph

def flux_to_prob(graph,already_sorted = True):
    nodeOutflux = dict()
    for edge in graph:
        if edge[0] not in nodeOutflux.keys():
            nodeOutflux[edge[0]] = edge[2]
        else:
            nodeOutflux[edge[0]] = nodeOutflux[edge[0]] + edge[2]
    return [(e[0],e[1],e[2]/nodeOutflux[e[0]]) for e in graph]

def impor(file):
    data = open(file).read().split('\n')
    data.pop(0)
    while data[-1]=='':
        data.pop(-1)
    for i,d in enumerate(data):
        d = d.replace(',', ' ')
        a,b,c = d.split()
        data[i]=(int(a),int(b),float(c))
    return data

def area(g0, g1, sort=False, complete=False):
    if complete:
        g0, g1 = complete_edges(g0,g1)
    if sort:
        g0.sort(key=lambda x: (x[0], x[1]))
        g1.sort(key=lambda x: (x[0], x[1]))
    return sum([abs(w-g1[i][2]) for i,(s,t,w) in enumerate(g0)])

def complete_edges(g0,g1):
    commonedges = set([(e[0],e[1],0) for e in g0+g1])
    c0 = list(commonedges - set([(e[0],e[1],0) for e in g0]))
    c1 = list(commonedges - set([(e[0],e[1],0) for e in g1]))
    return (g0 + c0,g1 + c1)

def WFCC(g0,g1, fVals = None, sort=False, complete = False):
    if complete:
        g0, g1 = complete_edges(g0,g1)
        sort = True
    if sort:
        g0.sort(key=lambda x: (x[0], x[1]))
        g1.sort(key=lambda x: (x[0], x[1]))
    if not (isinstance(g0, list) and isinstance(g1, list)):
        g0 = list(g0)
        g1 = list(g1)
    
    merged = [(min(w,g1[i][2]),max(w,g1[i][2])) for i,(s,t,w) in enumerate(g0)]
    
    #Finding the filtration values based on if the input is None, a number or a list.
    if not fVals:
        fVals = np.array(sorted(set(t[-1] for t in g0 + g1)))
        sCard = [0 for _ in fVals]
    else:
        try:
            sCard = [0 for _ in fVals]
            fVals = np.array(fVals)
        except:
            sCard = [0 for _ in range(fVals)]
            fVals = np.linspace(0, max(d for (_,d) in merged), fVals)
            
    for p0,p1 in merged:
        i = bisect_left(fVals,p0)
        while fVals[i]<p1:
            if fVals[i]<p0:
                i += 1
                continue
            sCard[i] += 1
            i += 1
    return (fVals,sCard)


def WFCCplot(g0, g1, label_g0, labels_g1, colors, log=False, fVals = None, sort=False, complete = False): 
    x,y = ([],[])
    for g in g1:
        x_val,y_val = WFCC(g0,g,fVals = fVals,sort=sort, complete=complete)
        x.append(x_val)
        y.append(y_val)
    fig,ax = plt.subplots(figsize=(6,5))
    for i in range(0, len(x)):
        plt.step(x[i],y[i], label=labels_g1[i], c=colors[i],where='post')
    plt.title(label_g0 + " compared to:", fontsize=15)
    plt.xlabel("Filtration value", fontsize=13)
    plt.ylabel("Cardinality of symmetric difference", fontsize=13)
    plt.legend(loc='best', fontsize=13)
    for label in (ax.get_xticklabels() + ax.get_yticklabels()):
        label.set_fontsize(13)
    if log==True:
        plt.yscale('log')
    plt.savefig('./Data_files_hypercubes/Outputs_github/'+label_g0+'_vs.png')
    plt.show()
    for i in range(0, len(x)):
        print("The area under the curve for "+label_g0+" vs "+labels_g1[i]+" is: ", area(g0,g1[i],sort,complete))