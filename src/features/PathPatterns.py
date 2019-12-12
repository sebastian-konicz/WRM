import pandas as pd
import nxviz as nv
import networkx as nx
import matplotlib.pyplot as plt
from pathlib import Path

def main(dir):
    RentalData = pd.read_csv(dir + r'\data\processed\RentalData2015.csv', delimiter=",", encoding="utf-8")
    RentalData = RentalData[RentalData['StartStation'] != "Aleja Bielany"]
    RentalData = RentalData[RentalData['EndStation'] != "Aleja Bielany"]

    graph = nx.from_pandas_edgelist(RentalData, source='StartStation', target='EndStation', edge_attr=True)
    print(graph.edges())
    print(graph.nodes())
    print(nx.info(graph))

    mtx = nv.MatrixPlot(graph)
    mtx.draw()
    cp = nv.CircosPlot(graph)
    cp.draw()

    degrees = [len(list(graph.neighbors(n))) for n in graph.nodes()]
    print(degrees)
    centrality = nx.degree_centrality(graph)
    print(centrality)



    nx.draw(graph)
    plt.show()

if __name__ == "__main__":
    project_dir = str(Path(__file__).resolve().parents[2])
    main(project_dir)