import networkx as nx
import matplotlib.pyplot as plt

def build_and_plot_graph(title, relationships):
    G = nx.DiGraph()

    for rel in relationships:
        G.add_node(rel['entity_1'])
        G.add_node(rel['entity_2'])
        G.add_edge(rel['entity_1'], rel['entity_2'], label=rel['relationship'])

    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=0.5)
    nx.draw(G, pos, with_labels=True, node_size=3000, node_color='skyblue', font_size=10, font_weight='bold', edge_color='gray')

    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    plt.title(f"Entity Relationship Knowledge Graph for: {title}")
    plt.show()
