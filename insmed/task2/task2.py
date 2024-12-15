"""
## Problem 2:
Your input is a file, where each line represents a roll of 6 dice.
Your task is to calculate the score of each roll according to the rules below.
Your final output should be the sum of the top 5 scores.

You should calculate the best possible score for the game, where a score can be assembled as a combination of a set of dice using the following rules:
- 1s not part of other combinations are worth 100 points each.
- 5s not part of other combinations are worth 50 points each.
- N>=3 of a kind is worth 100 × the face value of the die × (N - 2); e.g. 4 of a kind of 3s is worth 600 points.
- For the purpose of the rule above, the face value of a 1 is 10.
- A straight of N>4 dice is worth 1500 points.

A single die can only be part of one scoring combination, e.g. a straight from 1 to 5 would not include additional scores for 1s or 5s.
Where multiple scoring combinations are possible, you should choose the highest scoring combination.

Examples:
- ⚅ ⚀ ⚄ ⚀ ⚄ ⚄ - 3 of a kind of 5s, worth 500 points, plus two 1s worth 100 points each, giving a total of 700 points.
- ⚀ ⚀ ⚀ ⚀ ⚀ ⚀ - 6 of a kind of 1s, worth 4000 points.
- ⚀ ⚁ ⚂ ⚃ ⚄ ⚄ - Straight of 1 to 5, worth 1500 points, plus a single 5 worth 50 points, giving a total of 1550 points.


- [input_file](https://pastebin.com/raw/hmGFtGwa)
"""
DICE = {"⚀": 1, "⚁": 2, "⚂": 3, "⚃": 4, "⚄": 5, "⚅": 6}


def calculate_three_of_a_kind(play: list[int]):
    score = 0

    # Check if even worth calculating
    if len(play) < 3:
        return play, score

    def calculate_score(face, count):
        if face == 1:
            face = 10
        return 100 * face * (count - 2)

    counts = ((face, play.count(face)) for face in set(play))
    for face, count in counts:
        if count >= 3:
            # This can at most happen twice
            score += calculate_score(face, count)
            play = [x for x in play if x != face]

    return play, score

def calculate_straight(play: list[int]):
    """this has to be 1-5 or 2-6 to match the N>4 criteria"""
    str_play = "".join(map(str, play))
    # I know this isn't scalable for 7+ throws, but I've spent way too long on this already
    straights = ("12345", "23456")  # You could do something fun with range and len to generate a list of straights of N length though

    remainders = []
    for straight in straights:
        if straight in str_play:
            remainders.append(int("".join(str_play.split(straight))))  # This will isolate the non-straight value

    if remainders:
        return remainders, 1500
    return play, 0

def calculate_remainder(play: list[int]):
    """We only count 1 or 5"""
    score = 0
    for face in play:
        if face == 1:
            score += 100
        elif face == 5:
            score += 50

    return [x for x in play if x not in (1, 5)], score

def calculate_total_score(play: list[int]):
    score = 0
    for calculation in (calculate_straight, calculate_three_of_a_kind, calculate_remainder):
        outcome = calculation(play)
        play = outcome[0]  # we're shrinking
        score += outcome[1]

    return score

if __name__ == '__main__':
    scores = []
    with open("input.txt") as f:
        for line in f:
            play = [DICE[face] for face in line.strip().split()]
            scores.append(calculate_total_score(play))

    print(sum(sorted(scores, reverse=True)[:5]))

    """
    Outcome:
    7750
    """
