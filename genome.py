'''Filename: genome.py
Author: Michael Burman

This file contains the code for a class that is utilized for storing genome data of an organism.
It stores each organism's ID, genomic sequence, and n-grams.'''

class GenomeData:

    def __init__(self, name, genome):
        self._name = name
        self._genome = genome
        self._ngrams = None

    def get_name(self):
        return str(self._name)

    def get_genome(self):
        return str(self._genome)

    def get_ngrams(self):
        return set(self._ngrams)

    def set_ngrams(self, n):
        '''Pre-condition: Takes in a string of a genome and an integer.

        This method uses the integer and finds the corresponding amount of n-grams with length n via a list comprehension.

        Post-condition: Replaces self._ngrams with the set of ngrams.
        Code taken from cloud coder.'''
        s = set([self._genome[i:i + n] for i in range(len(self._genome) - n + 1)])
        self._ngrams = s
        return

    def compute_similarity(self, other):
        '''This method is used to compute the similarities of two different organisms by comparing each object's ngram set.
        Post-condition: Returns a float of the similarity value.'''
        self_ngrams = self._ngrams
        other_ngrams = GenomeData.get_ngrams(other)
        u = self_ngrams.union(other_ngrams)
        i = self_ngrams.intersection(other_ngrams)
        if self_ngrams == other_ngrams:
            return len(self_ngrams)/len(other_ngrams)
        return float(len(i)) / float(len(u))

    def __str__(self):
        return str(str(self._name))