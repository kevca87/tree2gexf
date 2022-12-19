import networkx as nx
import xml.etree.ElementTree as et

def get_xml_tree(file):
    tree = et.parse(file)
    return tree

def tree_2_gexf(tree,graph=None):
    if graph == None:
        graph = nx.Graph()
        root = tree.getroot()
        print(type(root))
    else:
        root = tree
    for node in root:
        graph.add_nodes_from([(f"{node.attrib['class']}.{node.attrib['methodName']}",node.attrib)])
        if 'methodName' in root.attrib :
            graph.add_edges_from([(f"{root.attrib['class']}.{root.attrib['methodName']}",f"{node.attrib['class']}.{node.attrib['methodName']}")])
        graph = tree_2_gexf(node,graph)
    return graph

tree = get_xml_tree('trees/vert.x-4.0.0_benchmarks.xml')
G = tree_2_gexf(tree)
nx.write_gexf(G, "geeksforgeeks.gexf")