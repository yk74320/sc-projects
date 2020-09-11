"""
File: Milestone1.py
Name: Ian Kuo
-----------------------
This file is to test the code for babyname.py milestone 1. If the name and/or ranking of a given year is
not in the assumed dictionary name_data, the program will add the data into it. Should both the name and
ranking of a given year already exists, the program will then replace the ranking with the highest one.
"""

import sys


def add_data_for_name(name_data, year, rank, name):
    year_rank = {year: rank}
    if name in name_data and year not in name_data[name]:
        name_data[name][year] = rank
    elif name in name_data and year in name_data[name]:
        old_rank = name_data[name][year]
        if rank < old_rank:
            name_data[name][year] = rank
    else:
        name_data[name] = year_rank



# ------------- DO NOT EDIT THE CODE BELOW THIS LINE ---------------- #

def test1():
    name_data = {'Kylie':{'2010':'57'}, 'Nick':{'2010':'37'}}
    add_data_for_name(name_data, '2010', '208', 'Kate')
    print('--------------------test1----------------------')
    print(str(name_data))
    print('-----------------------------------------------')


def test2():
    name_data = {'Kylie': {'2010': '57'}, 'Nick': {'2010': '37'}}
    add_data_for_name(name_data, '2000', '104', 'Kylie')
    print('--------------------test2----------------------')
    print(str(name_data))
    print('-----------------------------------------------')



def test3():
    name_data = {'Kylie': {'2010': '57'},'Sammy': {'1980':'451','1990': '200'}}
    add_data_for_name(name_data, '1990', '100', 'Sammy')
    print('-------------------test3-----------------------')
    print(str(name_data))
    print('-----------------------------------------------')


def test4():
    name_data = {'Kylie': {'2010': '57'}, 'Nick': {'2010': '37'}}
    add_data_for_name(name_data, '2010', '208', 'Kate')
    add_data_for_name(name_data, '2000', '108', 'Kate')
    add_data_for_name(name_data, '1990', '100', 'Sammy')
    add_data_for_name(name_data, '1990', '200', 'Sammy')
    add_data_for_name(name_data, '2000', '104', 'Kylie')
    print('--------------------test4----------------------')
    print(str(name_data))
    print('-----------------------------------------------')


def main():
    args = sys.argv[1:]
    if len(args) == 1 and args[0] == 'test1':
        test1()
    elif len(args) == 1 and args[0] == 'test2':
        test2()
    elif len(args) == 1 and args[0] == 'test3':
        test3()
    elif len(args) == 1 and args[0] == 'test4':
        test4()


if __name__ == "__main__":
    main()
