'''Filename: tree.py
Author: Michael Burman

This file contains the code for a class that is utilized for a tree data structure which utilizes a
phylogenic tree format.'''

class Tree:

    def __init__(self):
        self._name = None
        self._lchild = None
        self._rchild = None
        self._leaf = []

    def get_name(self):
        return str(self._name)

    def get_lchild(self):
        return self._lchild

    def get_rchild(self):
        return self._rchild

    def get_leaf(self):
        return self._leaf

    def set_leaf(self, val):
        '''This method sets the leaf for the tree to reference.'''
        if len(self._leaf) == 0 and type(val) == str:
            self._leaf.append(val)
        elif type(val) == list:
            self._leaf += val

    def set_name(self, val):
        self._name = val

    def adopt(self, tree1, tree2):
        '''This method takes in two trees and makes them the left and right children of the tree.'''
        if str(tree1) < str(tree2):
            self._lchild = tree1
            self._rchild = tree2
        else:
            self._lchild = tree2
            self._rchild = tree1

    def is_leaf(self):
        '''Pre-condition: Takes in an ID for an organism.

        This method checks to see if the tree is a leaf by verifying there is no left or right child.

        Post-conditon: Sets self._id to the ID value if verified to be a leaf of another tree.'''
        return self._lchild == None and self._rchild == None


    def __str__(self):
        if self.is_leaf():
            return self.get_name()
        else:
            return "({}, {})".format(str(self.get_lchild()), str(self.get_rchild()))