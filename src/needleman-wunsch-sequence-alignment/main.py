from needleman_wunsch import needleman_wunsch



# Print all alignments in convenient format
def print_alignment_beutify(first_seq, second_seq, alignment):
    print("".join("-" if e is None else first_seq[e] for e, _ in alignment))
    print("".join("-" if e is None else second_seq[e] for _, e in alignment))


print_alignment_beutify("ABC", "BC", needleman_wunsch("ABC", "BC"))
