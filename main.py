import os
import sys
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
        # print(type(root))
    else:
        root = tree
    for node in root:
        graph.add_nodes_from([(f"{node.attrib['class']}.{node.attrib['methodName']}",node.attrib)])
        if 'methodName' in root.attrib :
            graph.add_edges_from([(f"{root.attrib['class']}.{root.attrib['methodName']}",f"{node.attrib['class']}.{node.attrib['methodName']}")])
        graph = tree_2_gexf(node,graph)
    return graph

def get_xml_files_from(dir):
    return [t.split('.xml')[0] for t in os.listdir(dir) if '.xml' in t]

def get_trees_xml_files(in_dir_trees = IN_DIR_TREES, out_dir_graphs = OUT_DIR_GRAPHS, contain_subdir = False):
    trees_files_xml = get_xml_files_from(in_dir_trees)
    if contain_subdir:
        for directory in [d for d in os.listdir(in_dir_trees) if os.path.isdir(os.path.join(in_dir_trees, d))]:
            mkdir(f'{out_dir_graphs}/{directory}')
            directory_files = list(map(lambda t: f'{directory}/{t}',get_xml_files_from(f'{in_dir_trees}/{directory}')))
            trees_files_xml.extend(directory_files)
    return trees_files_xml

def mkdir(dir):
    try:
        os.mkdir(dir)
    except FileExistsError as exc:
        pass

def trees_2_graphs(in_dir_trees = IN_DIR_TREES, out_dir_graphs = OUT_DIR_GRAPHS, contain_subdir = False):
    trees_files_xml = get_trees_xml_files(in_dir_trees,out_dir_graphs,contain_subdir)
    for tree_file in trees_files_xml:
        tree = get_xml_tree(f'{in_dir_trees}/{tree_file}.xml')
        graph = tree_2_gexf(tree)
        nx.write_gexf(graph,f'{out_dir_graphs}/{tree_file}.gexf')
    print('Parsed files: ',trees_files_xml)

if __name__ == '__main__':
    contain_subdir = '-s' in sys.argv
    trees_2_graphs(contain_subdir=contain_subdir)