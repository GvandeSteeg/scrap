"""
## Problem 3:
The input is an unrefined macrodata set consisting of two-dimensional array of positive integers.
The rows are given as lines in the input file, with integers separated by commas to represent the columns.
Certain linearly-adjacent pairs of these integers invoke Dread and require refinement.
The output is a score representing the overall Dread in the macrodata set, measuring the extent to which the
data require further refinement.

- The overall Dread is the sum of the sums of Dread-invoking pairs, multiplied by the number of Dread-invoking pairs.
- A pair of linearly-adjacent numbers invokes Dread if their sum has 7 or 9 as a factor but not both. (e.g. 21, 45 but not 63)

Consider the input:

11, 19, 33, 64
14, 22, 47, 75
81, 14, 75, 82
9, 54, 41, 67

The Dread-invoking pairs are:

      -,-,-,-   -,-,-,-   -,-,-,-    -,-,-,-
      -,-,-,-   -,22,-,-  14,22,-,-  -,-,-,-
      81,-,-,-  -,14,-,-  -,-,-,-    -,-,-,-
      9,-,-,-   -,-,-,-   -,-,-,-    -,-,41,67

So the overall Dread is:
(90 + 36 + 36 + 108) * 4 = 1080

- [input_file](https://pastebin.com/raw/i7kJgsMR)
"""
from io import TextIOWrapper


def generate_matrix(file: TextIOWrapper) -> list[list[int]]:
    return [list(map(int, row.split(","))) for row in file]


def define_pairs(matrix: list[list[int]]):
    pairs: list[tuple[int]] = []
    for i, row in enumerate(matrix):
        for j, column in enumerate(row):
            try:
                pairs.append((matrix[i][j], matrix[i][j + 1]))  # horizontal
                pairs.append((matrix[j][i], matrix[j + 1][i]))  # vertical
            except IndexError:
                pass

    return pairs


def define_dread(pair: tuple[int, int]):
    """This is just FizzBuzz"""
    sump = sum(pair)
    outcomes = [sump % 7 == 0, sump % 9 == 0]
    if any(outcomes) and not all(outcomes):
        return sump, True
    return 0, False


def calculate_overall_dread(dreads: list[tuple[int, bool]]):
    dread = [d[0] for d in dreads if d[1]]
    overall_dread = sum(dread) * len(dread)
    return overall_dread


if __name__ == "__main__":
    with open("input.txt") as f:
        matrix = generate_matrix(f)

    pairs = define_pairs(matrix)
    dread = [define_dread(pair) for pair in pairs]
    overall_dread = calculate_overall_dread(dread)

    print(overall_dread)

    """
    Outcome:
    147961342
    """
