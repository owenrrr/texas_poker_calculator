#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import numpy as np
import collections
import poker_table as pt
import view as vw

Number = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
Ind2Number = dict(zip([i for i in range(13)], Number))
Number2Ind = dict(zip(Number, [i for i in range(13)]))

def test_royal_flush():
    hands = [10, 11]
    flop = [12, 13, 1]
    turn = [44]
    river = [30]
    flag, set = print_results(hands, flop, turn, river, Ind2Number)


def test_straight_flush():
    hands = [4, 5]
    flop = [6, 7, 8]
    turn = [9]
    river = [35]
    flag, set = print_results(hands, flop, turn, river, Ind2Number)


def test_four_kind():
    hands = [1, 14]
    flop = [27, 40, 3]
    turn = [9]
    river = [36]
    flag, set = print_results(hands, flop, turn, river, Ind2Number)
    assert flag == 'Four-of-a-Kind'
    assert set == ['A', 'A', 'A', 'A', '10']


def test_full_house():
    hands = [9, 22]
    flop = [35, 10, 23]
    turn = [36]
    river = [40]
    flag, set = print_results(hands, flop, turn, river, Ind2Number)
    assert flag == 'Full House'
    assert set == ['10', '10', '10', '9', '9']


def test_flush():
    hands = [14, 17]    # A, 4
    flop = [20, 23, 24] # 7, 10, J
    turn = [38]
    river = [26] # K
    flag, set = print_results(hands, flop, turn, river, Ind2Number)

    assert flag == 'Flush'
    assert set == ['7', '10', 'J', 'K', 'A']


def test_straight():
    hands = [27, 30]  # A, 4
    flop = [7, 23, 24]  # 7, 10, J
    turn = [51] # Q
    river = [26]  # K
    flag, set = print_results(hands, flop, turn, river, Ind2Number)

    assert flag == 'Straight'
    assert set == ['10', 'J', 'Q', 'K', 'A']


def test_three_kind():
    hands = [3, 16]  # 3, 3
    flop = [7, 23, 24]  # 7, 10, J
    turn = [42]  # 3
    river = [40]  # A
    flag, set = print_results(hands, flop, turn, river, Ind2Number)

    assert flag == 'Three-of-a-Kind'
    assert set == ['3', '3', '3', 'J', 'A']


def test_two_pairs():
    hands = [3, 16]  # 3, 3
    flop = [7, 23, 24]  # 7, 10, J
    turn = [46]  # 7
    river = [40]  # A
    flag, set = print_results(hands, flop, turn, river, Ind2Number)

    assert flag == 'Two Pairs'
    assert set == ['3', '3', '7', '7', 'A']


def test_one_pair():
    hands = [3, 16]  # 3, 3
    flop = [7, 23, 26]  # 7, 10, K
    turn = [45]  # 6
    river = [40]  # A
    flag, set = print_results(hands, flop, turn, river, Ind2Number)

    assert flag == 'One Pair'
    assert set == ['3', '3', '10', 'K', 'A']


def test_no_pair():
    hands = [3, 17]  # 3, 4
    flop = [7, 23, 26]  # 7, 10, K
    turn = [45]  # 6
    river = [40]  # A
    flag, set = print_results(hands, flop, turn, river, Ind2Number)

    assert flag == 'No Pair'
    assert set == ['6', '7', '10', 'K', 'A']


def print_results(hands, flop, turn, river, Ind2Number):
    flag, set = vw.get_set(hands, flop, turn, river)
    set = [Ind2Number[item] for item in set]
    print(flag, set)
    return flag, set


def all_test():
    test_royal_flush()
    test_straight_flush()
    test_four_kind()
    test_full_house()
    test_flush()
    test_straight()
    test_three_kind()
    test_two_pairs()
    test_one_pair()
    test_no_pair()


if __name__ == '__main__':
    # all_test()
    vw.viewer()





