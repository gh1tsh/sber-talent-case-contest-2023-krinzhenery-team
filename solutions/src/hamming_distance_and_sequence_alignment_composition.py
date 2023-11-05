# File: hamming_distance_and_sequence_alignment_composition.py
# Created on 04.11.2023 at 22:04
# Author: ghitsh
#
# Description: This file contains the implementation of the composition of the
# sequence alignment algorithm (as an auxiliary) and the Hamming distance
# algorithm.

from needleman_wunsch import needleman_wunsch



def hamming_distance_normalized(left: str, right: str) -> float:

    # left, right - sequences of words separated by spaces (sentences or texts)

    aligned_sequences_sample = [] # A list of tuples containing the indexes of
                                  # the original sequences

    seq_1 = left.split(' ')
    seq_2 = right.split(' ')
    
    first_seq_aligned = []
    second_seq_aligned = []

    if len(seq_1) != len(seq_2):
        aligned_sequences_sample = needleman_wunsch(seq_1, seq_2)
        for i, j in aligned_sequences_sample:
            first_seq_aligned.append(("-" * len(seq_2[j]) if i is None else seq_1[i]))
            second_seq_aligned.append(("-" * len(seq_1[i])) if j is None else seq_2[j])
    else:
        first_seq_aligned = seq_1
        second_seq_aligned = seq_2

    d = 0 # Hamming's distance
    for i in range(len(first_seq_aligned)):
        d += first_seq_aligned[i] != second_seq_aligned[i]

    return 1 - (d / max(len(seq_1), len(seq_2))) # Simple metric

def is_rewrite_hamming_distance_normalized(left: str, right: str, threshold: float) -> bool:
    # left, right - sequences of words separated by spaces (sentences or texts)
    #
    # threshold - some value (defined by user) which determines whether
    # a given sequence of words is rewrite.
    return hamming_distance_normalized(left,right) > threshold