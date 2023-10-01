import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
from dataStructure import *

def displayAllNodesinGraph():
    edges = pd.read_csv('coordinates.csv', names=['city', 'longitude', 'latitude'])
    with open("adjacencies.txt") as f:
        adjacencies = f.readlines()

    city = weightedBidirectionalGraph(edges, adjacencies)
    G = nx.Graph()
    for i in adjacencies:
        city1, city2 = i.split()
        cost = city.euclidDistance(city.getCoordinate(city1), city.getCoordinate(city2))
        G.add_edge(city1, city2, weight=cost)

    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 0.5]
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 0.5]

    # positions for all nodes - seed for reproducibility
    pos = nx.spring_layout(G, seed=7)  

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=70)

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=elarge, width=6)
    nx.draw_networkx_edges(G, pos, edgelist=esmall, width=10, alpha=0.5, edge_color="b")

    # node labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")

    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.show()

def displayGraphImage(nodes):
    edges = pd.read_csv('coordinates.csv', names=['city', 'longitude', 'latitude'])
    with open("adjacencies.txt") as f:
        adjacencies = f.readlines()
        
    city = weightedBidirectionalGraph(edges, adjacencies)

    G = nx.Graph()
    for i in range(len(nodes)-1):
        cost = city.euclidDistance(city.getCoordinate(nodes[i]), city.getCoordinate(nodes[i+1]))
        G.add_edge(nodes[i], nodes[i+1], weight=cost)

    elarge = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] > 0.5]
    esmall = [(u, v) for (u, v, d) in G.edges(data=True) if d["weight"] <= 0.5]

    # positions for all nodes - seed for reproducibility
    pos = nx.spring_layout(G, seed=7)  

    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=200)

    # edges
    nx.draw_networkx_edges(G, pos, edgelist=elarge, width=6)
    nx.draw_networkx_edges(G, pos, edgelist=esmall, width=10, alpha=0.5, edge_color="b")

    # node labels
    nx.draw_networkx_labels(G, pos, font_size=10, font_family="sans-serif")

    # edge weight labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels)

    ax = plt.gca()
    ax.margins(0.08)
    plt.axis("off")
    plt.tight_layout()
    plt.show()