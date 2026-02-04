from Levenshtein import ratio
from sklearn.metrics.pairwise import cosine_similarity

import networkx as nx
import matplotlib
import matplotlib.pyplot as plt
import pygraphviz

def levenshtein_sim(m1, m2): 
    """
        Computes similarity based on string-edit distance, see:
        https://en.wikipedia.org/wiki/Levenshtein_distance
        
        :m1 Character string, module 1 title
        :m2 Character string, module 2 title
        :returns float, measure of similarity between 0 and 1; 1 is identical, 0 is most dissimilar
    """
    return ratio(m1.lower(), m2.lower())

def jacc_sim(k1, k2):
    """
        Computes Jaccard similarity metric, see:
        https://en.wikipedia.org/wiki/Jaccard_index
        
        :k1 character string with key concepts in module 1, e.g. "datum, probability"
        :k2 character string with key concepts in module 2, e.g. "datum, probability, machine learning"
        :returns float, between 0 and 1; 1 is most similar.
    """
    k1 = [x.strip() for x in k1.split(',')]
    k2 = [x.strip() for x in k2.split(',')]
    u1 = set(k1).union(set(k2))
    i1 = set(k1).intersection(set(k2))
    return len(i1)/len(u1)

def satisfies_prerequisites(prereq_tree, passed_modules):
    """
    Recursively checks if the student meets the prerequisite tree requirements.
    Written by Mr Chat GPT

    :param prereq_tree: dict or str, a nested prerequisite tree
    :param passed_modules: set of modules the student has passed (e.g., {'BT1101:D', 'MA1101R:D'})
    :return: bool, whether the student satisfies the prerequisites
    """
    if isinstance(prereq_tree, str):
        if '%' in prereq_tree:
            prefix = prereq_tree.split('%')[0]
            return any(mod.startswith(prefix) for mod in passed_modules)
        return prereq_tree in passed_modules

    elif isinstance(prereq_tree, dict):
        if 'and' in prereq_tree:
            return all(satisfies_prerequisites(subtree, passed_modules) for subtree in prereq_tree['and'])
        elif 'or' in prereq_tree:
            return any(satisfies_prerequisites(subtree, passed_modules) for subtree in prereq_tree['or'])

    return False

# plotting graph

def build_graph_from_prereq(prereq_tree):
    G = nx.DiGraph()
    _ = _build_graph_recursive(prereq_tree, G, None, {'id': 0})
    return G

def _build_graph_recursive(prereq_tree, graph, parent, counter):
    if isinstance(prereq_tree, str):
        node_id = prereq_tree
    elif isinstance(prereq_tree, dict):
        logic = list(prereq_tree.keys())[0]  # "and" or "or"
        node_id = f"{logic.upper()}_{counter['id']}"
        counter['id'] += 1
        graph.add_node(node_id, label=logic.upper())
        for child in prereq_tree[logic]:
            child_id = _build_graph_recursive(child, graph, node_id, counter)
            graph.add_edge(node_id, child_id)
    else:
        raise ValueError("Unexpected node type")

    if parent:
        graph.add_edge(parent, node_id)

    return node_id

def draw_prereq_graph(graph):
    pos = nx.nx_agraph.graphviz_layout(graph, prog="dot")
    labels = {node: graph.nodes[node].get("label", node) for node in graph.nodes()}
    nx.draw(graph, pos, with_labels=True, labels=labels, node_size=300,
            node_color="lightblue", font_size=5, font_weight='regular', arrows=True)
    plt.title("Prerequisite Tree")
    plt.savefig('test.png')
