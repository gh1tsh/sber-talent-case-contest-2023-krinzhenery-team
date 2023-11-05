from itertools import product
from collections import deque



def needleman_wunsch(left, right):
    # This is Needleman-Wunsch sequence alignment algorithm implementation.
    # Time complexity: O(n * m) where n, m - lengths of sequences
    #
    # left, right: any iterable sequences.

    N, M = len(left), len(right)
    s = lambda a, b: int(a == b)

    DIAG = (-1, -1)
    LEFT = (-1, 0)
    UP = (0, -1)

    F = {}
    Ptr = {}

    F[-1, -1] = 0
    for i in range(N):
        F[i, -1] = -i
    for j in range(M):
        F[-1, j] = -j

    option_Ptr = (DIAG, LEFT, UP)

    for i, j in product(range(N), range(M)):
        option_F = (
            F[i - 1, j - 1] + s(left[i], right[j]),
            F[i - 1, j] - 1,
            F[i, j - 1] - 1,
        )
        F[i, j], Ptr[i, j] = max(zip(option_F, option_Ptr))

    alignment = deque()
    i, j = N - 1, M - 1
    while i >= 0 and j >= 0:
        direction = Ptr[i, j]
        if direction == DIAG:
            element = i, j
        elif direction == LEFT:
            element = i, None
        elif direction == UP:
            element = None, j
        alignment.appendleft(element)
        di, dj = direction
        i, j = i + di, j + dj
    while i >= 0:
        alignment.appendleft((i, None))
        i -= 1
    while j >= 0:
        alignment.appendleft((None, j))
        j -= 1

    return alignment

# Print all alignments in convenient format
def print_alignment_beautify(first_seq, second_seq, alignment):
    print("".join("-" if e is None else first_seq[e] for e, _ in alignment))
    print("".join("-" if e is None else second_seq[e] for _, e in alignment))
