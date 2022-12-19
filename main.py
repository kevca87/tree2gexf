import os
import networkx as nx
import xml.etree.ElementTree as et

OUT_DIR_GRAPHS = 'gexf'
IN_DIR_TREES = 'trees'

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

def trees_2_graphs(in_dir_trees = IN_DIR_TREES,out_dir_graphs = OUT_DIR_GRAPHS):
    trees_files_xml = [t.split('.xml')[0] for t in os.listdir(in_dir_trees) if '.xml' in t]
    print(trees_files_xml)
    for tree_file in trees_files_xml:
        tree = get_xml_tree(f'{in_dir_trees}/{tree_file}.xml')
        graph = tree_2_gexf(tree)
        nx.write_gexf(graph,f'{out_dir_graphs}/{tree_file}.gexf')

if __name__ == '__main__':
    trees_2_graphs()