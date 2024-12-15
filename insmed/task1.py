"""
## Problem 1:
Find the consensus sequence from a list of sequences, where the input is a file with each
line representing a sequence of nucleotides. The consensus sequence is the most common
nucleotide at each position in the sequences.

In the case of a tie, the consensus sequence should be 'N'.

Calculate the score of the consensus sequence by summing the values of each nucleotide
according to the following values:
A = 2, C = 5, G = 3, T = 4, N = -1

Example:
- ACGAT
- CCGATGG
- ACGA
- TCGAG
- ACGAG

The consensus sequence is 'ACGANGG' and the score is 2+5+3+2-1+3+3 = 17

- [input_file](https://pastebin.com/raw/hHzaMRua)
"""
from copy import copy
from io import TextIOWrapper

finput = "input.txt"


class Nucleotides:
    def __init__(self, A=0, C=0, G=0, T=0):
        self.A = A
        self.C = C
        self.G = G
        self.T = T

    def generate_consensus_character(self):
        """Returns highest scoring nucleotide for a position or N if more than 1 shares the highest score"""
        highest = max(self.A, self.C, self.G, self.T)
        if list(vars(self).values()).count(highest) > 1:
            return "N"
        else:
            return next(k for k, v in vars(self).items() if v == highest)


def count_nucleotides_in_position(file: TextIOWrapper):
    nucleotides = dict(A=0, C=0, G=0, T=0)

    scores = []
    for line in file:
        line = line.strip()
        if not line:
            continue

        for i, nucleotide in enumerate(line):
            try:
                scores[i][nucleotide] += 1
            except IndexError:
                scores.append(copy(nucleotides))
                scores[i][nucleotide] += 1
    return scores


def generate_consensus(scores):
    consensus = ""
    for position in scores:
        pos = Nucleotides(**position)
        consensus += pos.generate_consensus_character()
    return consensus


def calculate_score(consensus):
    scoring_sheet = dict(A=2, C=5, G=3, T=4, N=-1)
    return sum(scoring_sheet[n] for n in consensus)


if __name__ == "__main__":
    with open(finput) as f:
        counts = count_nucleotides_in_position(f)

    consensus = generate_consensus(counts)
    score = calculate_score(consensus)

    print(consensus)
    print(score)

    """
    Output:
    GTATTGTTCTCTCTGTAGTATCGGCTNTAACCCGTANCGGATCATGTAATTCAAANAATACCCTNCNGGGCAGANCAGGAGGNTCAGCATCAAGNTCATG
    310
    """
