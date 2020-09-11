"""
File: similarity.py
Name: Ian Kuo
----------------------------
This program compares short dna sequence, s2,
with sub sequences of a long dna sequence, s1
The way of approaching this task is the same as
what people are doing in the bio industry.
"""


def main():
    """
    The objective of this program is to discover the homology of two DNA strand sequences. The user inserts one
    strand to be searched, determined as the long sequence, and another one to be matched, determined as the
    short sequence. Once compared, the program returns a sequence that has the highest similarity.
    """
    long_sequence = input('Please insert a DNA strand sequence to be searched: ')
    long_sequence = long_sequence.upper()
    short_sequence = input('What DNA sequence would you like to be matched: ')
    short_sequence = short_sequence.upper()
    len_l = len(long_sequence)
    len_s = len(short_sequence)
    score = 0
    max = score
    ans = ''

    for i in range(len_l - len_s + 1):
        for j in range(len_s):
            ch_l = long_sequence[i + j]
            ch_s = short_sequence[j]
            if ch_l == ch_s:
                score += 1
            else:
                score -= 0
        if max < score:
            max = score
            ans = long_sequence[i:i+len_s]
            sim = (max / len_s) * 100
        score = 0
    print('The best match of the strand is ' + ans)
    print('The similarity percentage of the match is ' + str(sim) + '%')


###### DO NOT EDIT CODE BELOW THIS LINE ######
if __name__ == '__main__':
    main()
