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

def nodeNear(G,delta):
    f=10000
    pos=nx.get_node_attributes(G,'pos')
    for n in pos:
        x1,y1=pos[n]
        for i in G.neighbors(n):
            x2,y2=pos[i]
            d=(x1-x2)**2+(y1-y2)**2
            if d<delta:
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
     #       print "ERROR: genRandomGeorml <nodes> <raio> <delta>"
      #      sys.exit(1)

    NMAX = int(sys.argv[1])
    RAIO = float(sys.argv[2])
    delta = float(sys.argv[3])
    #NMAX=40
    #RAIO=0.1
    ALCANCE=250
    c=0

    first=True
    while True:
        G=nx.random_geometric_graph(NMAX,RAIO,2)

        while not nx.is_connected(G):
            c+=1
            if first: RAIO=RAIO+.005
            G=nx.random_geometric_graph(NMAX,RAIO,2)
            if LOG: print c,"- Radius: Graph is not full connected"
        first=False

        pos=nx.get_node_attributes(G,'pos')
        #network(G,pos,1)

        #Remove vizinhos que estejam demasiado perto
        while nodeNear(G,delta)<1000 :
            G.remove_node(nodeNear(G,delta))

        pos=nx.get_node_attributes(G,'pos')
        #network(G,pos,2)
        if nx.is_connected(G):
            #Remove no que tem mais vizinhos
            candidate=nodeMaxDegree(G)
            while nx.degree(G,candidate)> 4 :
                if not nodeSolo(G,candidate):
                    G.remove_node(candidate)
                    candidate=nodeMaxDegree(G)
                    
            #network(G,pos,3)
            if nx.is_connected(G):
                pos=nx.get_node_attributes(G,'pos')
                #Remove 
                for n in G.neighbors(nodeMaxDegree(G)):
                    if nx.degree(G,n)== 2 :
                        degree=nx.degree(G,n)
                        node=n
                        print "Extra node=",n
                        if not nodeSolo(G,n): G.remove_node(n)
                        #break
                if nx.is_connected(G):
                    if LOG: print "Start:",NMAX,"End:",G.number_of_nodes()
                    pos=nx.get_node_attributes(G,'pos')
                    network(G,pos,4)
                    break
            else:
                c+=1
                if LOG: print c,"- MaxDegree: Split Graph" 
        else:
            c+=1
            if LOG: print c,"- NearNode: Split Graph"




if __name__ == "__main__":
    print main()
