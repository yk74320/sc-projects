"""
File: caesar.py
Name: Ian Kuo
------------------------------
This program demonstrates the idea of caesar cipher.
Users will be asked to input a number to produce shifted
ALPHABET as the cipher table. After that, any strings typed
in will be encrypted.
"""


# This constant shows the original order of alphabetic sequence
ALPHABET = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'


def main():
    """
    The objective of this program is to decrypt a given cipher using a code book that contains a shifted ALPHABET
    sequence, with the number of shifts determined by the inserted secret number.
    """
    secret = int(input('Please enter your secret number: '))
    new_alpha = traverse(secret)
    print('The encrypted code sequence is:' + new_alpha)
    ans = ''
    cipher = input('What is the ciphered string? ')
    cipher = cipher.upper()
    for i in range(len(cipher)):
        ch = cipher[i]
        c_code = new_alpha.find(ch)
        if c_code != -1:
            d_code = ALPHABET[c_code]
        else:
            d_code = ch
        ans += d_code
    print('The deciphered string is: ' + ans)


def traverse(secret):
    """
    :param secret: int, number of ALPHABET sequence shift
    :return: str, the new ALPHABET sequence
    """
    new_alpha = ''
    new_alpha += ALPHABET[26 - secret:26]
    new_alpha += ALPHABET[:26 - secret]
    return new_alpha


#####  DO NOT EDIT THE CODE BELOW THIS LINE  #####
if __name__ == '__main__':
    main()
