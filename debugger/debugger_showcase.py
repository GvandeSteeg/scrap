from pprint import pprint
from typing import Dict


def fasta_parser(fasta_path: str) -> Dict[str, str]:
    parsed = {}
    with open(fasta_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith(">"):
                key = line[1:]
                parsed[key] = ""
            else:
                parsed[key] += line
    return parsed


def reverse_complement(seq_string: str) -> str:
    compl = dict(A="T", T="A", G="C", C="G")
    new_str = [compl[i.upper()] for i in seq_string]
    return "".join(new_str)


fasta_d = fasta_parser("brca2.fa")
pprint(fasta_d)
for seq in fasta_d.values():
    print(reverse_complement(seq))
