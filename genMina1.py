#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-
import scipy as sp
import numpy as np
import networkx as nx
import random as rnd
import matplotlib.pyplot as plt
import math
import sys


def nodeMaxDegree(G):
    degree=0
    for n in G.nodes():
        if nx.degree(G,n)> degree :
            degree=nx.degree(G,n)
            node=n
    return node

def nodeSolo(G,n):
    solo=False
    for test in G.neighbors(n):
        if nx.degree(G,test)== 1 :
            solo=True
    return solo

def nodeNear(G):
    f=10000
    pos=nx.get_node_attributes(G,'pos')
    for n in pos:
        x1,y1=pos[n]
        for i in G.neighbors(n):
            x2,y2=pos[i]
            d=(x1-x2)**2+(y1-y2)**2
            if d<0.006 :
                f=i
                break
    return f
        

def network(G,pos,seq):
    plt.clf()
    nx.draw_networkx_nodes(G,pos,node_color='#FFFF00') 
    nx.draw_networkx_edges(G,pos)
    nx.draw_networkx_labels(G,pos)
    plt.axis('off')
    plt.savefig("./network%d.png" % seq)
    plt.show()
    return True


def main():
    LOG = True

    #if (len(sys.argv) != 3):
     #       print "ERROR: genRandomGeorml <nodes> <raio>"
      #      sys.exit(1)

    NMAX = int(sys.argv[1])
    RAIO = float(sys.argv[2])
    #NMAX=40
    #RAIO=0.1
    ALCANCE=250

    G=nx.random_geometric_graph(NMAX,RAIO,2)

    while not nx.is_connected(G):
         RAIO=RAIO+.005
         G=nx.random_geometric_graph(NMAX,RAIO,2)
         if LOG: print "Graph is not full connected"

    pos=nx.get_node_attributes(G,'pos')
    network(G,pos,1)

    #Remove vizinhos que estejam demasiado perto
    while nodeNear(G)<1000 :
        G.remove_node(nodeNear(G))

    if nx.is_connected(G):
        pos=nx.get_node_attributes(G,'pos')
        network(G,pos,2)

        #Remove no que tem mais vizinhos
        T=G
        if not nodeSolo(T,nodeMaxDegree(T)): T.remove_node(nodeMaxDegree(T))
        if nx.is_connected(T):
                G=T

        pos=nx.get_node_attributes(G,'pos')
        network(G,pos,3)



        for n in G.neighbors(nodeMaxDegree(G)):
            if nx.degree(G,n)== 2 :
                degree=nx.degree(G,n)
                node=n
                print "node=",n
                if not nodeSolo(G,n): G.remove_node(n)
                break
        
        pos=nx.get_node_attributes(G,'pos')
        network(G,pos,4)
    else:
        if LOG: print "SubGraph is not full connected"


if __name__ == "__main__":
    print main()
