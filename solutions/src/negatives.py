def count_negatives(line):
    words = line.split()
    negations = ["не", "ни"]
    negation_counters = [0] * len(negations)
    for word in words:
        for i in range(len(negations)):
            if word.startswith(negations[i]):
                negation_counters[i] += 1
    return sum(negation_counters)

def check_negative_corresponense(line1, line2):
    return (count_negatives(line1) % 2) == (count_negatives(line2) % 2)