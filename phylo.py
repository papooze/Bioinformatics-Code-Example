from genome import *
from tree import *

'''Filename: phylo.py
Author: Michael Burman

This program takes in two inputs, the first being the name of a FASTA file in text format, and the second being an integer.

It first reads the file, and extracts each organism's ID and genome sequence, and organizes them into a dictionary,
with the ID being the key and the genome being its value.

It then finds each of the N-grams for each organism, specified by the second input and saves them as a set to replace the value
inside of the original dictionary.

It then finds the similarity of each organism using the Jaccard index, and returns the similarity as a float.

Then, it uses these similarity values to compute a phylogenic tree.

Finally, it prints out the phylogenic tree in a string format.'''

def read_file_data():
    '''Pre condition: A FASTA text file is inputted in this function.
    Post condition: the text file is read and returns a dictionary of organisms and related genomic sequences.'''
    name = ""
    gen = ""
    organism_dict = {}
    name_file = input("FASTA file: ")
    try:
        name_file = open(name_file)
    except IOError:
        print("n-gram size: "+"ERROR: could not open file", str(name_file))
        quit()
    while True:
        line = name_file.readline()
        if line == "":
            break
        if line[0] == ">":
            line = line[1:].split()
            name = line[0]
        elif line[0].isalpha():
            gen += line
        else:
            gen = gen.replace('\n', '')
            organism_dict[name] = gen
            gen = ""
    name_file.close()
    return organism_dict

def create_organism_objects(organism_dict):
    '''Pre-condition: Takes in a dictionary of organisms and associated genomes.

    This function first takes in an input of an integer that it uses to compute n-grams for each of the organisms
    inside of the dictionary. After it does, it adds each object to a list of organism objects.

    Post-condition: Returns a list of organism objects with computed ngrams.'''
    org_objects = []
    N = input('n-gram size: ')
    try:
        N = int(N)
    except ValueError:
        print("ERROR: Bad value for N")
        quit()
    for organism in organism_dict.keys():
        org = GenomeData(organism, organism_dict[organism])
        GenomeData.set_ngrams(org, N)
        org_objects.append(org)
    return org_objects

def compute_similarities(organism_objects):
    '''Pre-condition: This function takes in a list of organism objects.

    This function computes the similarities of each organism by taking each organism and comparing it to one another
    via the use of the enumerate method.
    It saves the similarity value in a dictionary, which is organized by the names of the two organisms as the key, and
    their similarity value as the dictionary value.

    Post-condition: Returns a dictionary of organism comparisons with their similarity values.'''
    comparison_dict = {}
    for i, org in enumerate(organism_objects):
        for other_org in organism_objects[i + 1:]:
            sim_value = GenomeData.compute_similarity(org, other_org)
            tup = ((GenomeData.get_name(org), (GenomeData.get_name(other_org))))
            tup2 = ((GenomeData.get_name(other_org), GenomeData.get_name(org)))
            comparison_dict[tup] = sim_value
            comparison_dict[tup2] = sim_value
    return comparison_dict

def leaf_compare(comparison_dict, t1, t2):
    '''This function is a helper function for max_of_two_trees(). It returns the maximum value of two leaves.'''
    maximum = 0
    maxi_name = ()
    dist = 0
    for leaf in t1.get_leaf():
        for leaf2 in t2.get_leaf():
            if leaf != leaf2:
                dist = comparison_dict[leaf, leaf2]
                if dist > maximum:
                    maximum = dist
                    maxi_name = leaf, leaf2
    return maximum

def max_of_two_trees(comparison_dict, tree_list):
    '''Pre-condition: This function takes in a dictionary of values and a list of trees.

    Post-condition: returns a tuple of tree objects.'''
    max_of_two = 0
    t = ()
    for tree in tree_list:
        for other_tree in tree_list:
            if tree == other_tree:
                continue
            max_o = leaf_compare(comparison_dict, tree, other_tree)
            if max_o > max_of_two:
                max_of_two = max_o
                t = tree, other_tree
    return t





def create_phylogenic_tree(comparison_dict, organism_objects):
    '''Pre-condition: Takes in a dictionary of organism comparisons.

    This program takes a dictionary of all the comparisons of the organisms and organizes them in a hierarchical format
    based on the values of the comparison.

    Post-condition: Returns a phylogenic tree in string format.'''
    tree_list = []
    for organism in organism_objects:
        tree = Tree()
        tree.set_name(organism)
        tree.set_leaf(GenomeData.get_name(organism))
        tree_list.append(tree)
    while len(tree_list) > 1:
        tup = max_of_two_trees(comparison_dict, tree_list)
        blank_tree = Tree()
        leaf1 = tup[0].get_leaf()
        leaf2 = tup[1].get_leaf()
        blank_tree.set_leaf(leaf1)
        blank_tree.set_leaf(leaf2)
        Tree.adopt(blank_tree, tup[0], tup[1])
        tree_list.remove(tup[0])
        tree_list.remove(tup[1])
        tree_list.append(blank_tree)
    print(tree_list[0])






def main():
    organism_dict = read_file_data()
    organism_objects = create_organism_objects(organism_dict)
    comparison_dict = compute_similarities(organism_objects)
    create_phylogenic_tree(comparison_dict, organism_objects)

main()
