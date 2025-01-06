import matplotlib.pyplot as plt
import pandas as pd
import networkx as nx
import math

import math

def compute_distance(coord1, coord2):
    R = 6371.0
    
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    distance = R * c
    return distance

def generate_graph_from_csv(csv_file):
    data = pd.read_csv(csv_file)
    G = nx.Graph()
    pos = {}
    for index, row in data.iterrows():
        pos[row['Name']] = (row['Longitude'], row['Latitude'])
        G.add_node(row['Name'], pos=(row['Longitude'], row['Latitude']))
    return G, pos

def calculate_distance(pos1, pos2):
    return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2) ** 0.5

def build_edges(G, nodes):
    G.clear_edges()
    for i, node1 in enumerate(nodes):
        distances = []
        for j, node2 in enumerate(nodes):
            if i != j:
                pos1 = node1[1]['pos']
                pos2 = node2[1]['pos']
                distance = calculate_distance(pos1, pos2)
                distances.append((node1[0], node2[0], distance))
        distances = sorted(distances, key=lambda x: x[2])[:3]
        for edge in distances:
            G.add_edge(edge[0], edge[1], weight=edge[2])
    return G

def ids(graf, start, tujuan, kedalaman_maks):
    def dls(simpul, tujuan, kedalaman, dikunjungi, jalur_koordinat):
        if simpul == tujuan:
            return True, jalur_koordinat + [(simpul, graf.nodes[simpul]['pos'])]
        if kedalaman == 0:
            return False, jalur_koordinat
        for tetangga in graf.neighbors(simpul):
            if tetangga not in dikunjungi:
                dikunjungi.add(tetangga)
                ditemukan, koordinat_baru = dls(tetangga, tujuan, kedalaman - 1, dikunjungi, jalur_koordinat + [(simpul, graf.nodes[simpul]['pos'])])
                if ditemukan:
                    return True, koordinat_baru
                dikunjungi.remove(tetangga)
        return False, jalur_koordinat

    for kedalaman in range(kedalaman_maks):
        dikunjungi = set([start])
        ditemukan, koordinat = dls(start, tujuan, kedalaman, dikunjungi, [])
        if ditemukan:
            return koordinat 
    return None  

def find_path(csv_file, node_awal, goal_node, kedalaman_maks):
    G, pos = generate_graph_from_csv(csv_file)
    nodes = list(G.nodes(data=True))
    G = build_edges(G, nodes)
    
    koordinat_jalur = ids(G, node_awal, goal_node, kedalaman_maks)

    if koordinat_jalur:
        print("Node yang dilewati:")
        for simpul, lat_lon in koordinat_jalur:
            print(f"{simpul}: {lat_lon}")
    else:
        print(f"Tidak ditemukan jalur dari {node_awal} ke {goal_node}")

    path_dict = {}
    if koordinat_jalur:
        for simpul, (lat, lon) in koordinat_jalur:
            path_dict[simpul] = {'Latitude': lat, 'Longitude': lon}
    
    return path_dict
