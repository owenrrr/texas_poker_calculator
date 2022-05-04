#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import numpy as np
import collections


class PokerTable:

    def __init__(self,
                 hands=None,
                 player=2):
        """
        hands: [x, y], 1<= x,y <= 52 , counts A,2,3,...,Q,K; color counts Club Diamond Heart Spade
        example: own:[13, 46] means player has Club K and Spade 7
        :param player: int, how many players
        :param hands: shape[2], represents your hands poker
        """
        ind = [i for i in range(10)]
        nuts = ['No Pair', 'One Pair', 'Two Pairs', 'Three-of-a-Kind', 'Straight',
                'Flush', 'Full House', 'Four-of-a-Kind', 'Straight Flush', 'Royal Flush']
        self.Ind2Nut = dict(zip(ind, nuts))
        self.Nut2Ind = dict(zip(nuts, ind))
        self.player = player
        self.phase = 'pre-flop'
        self.table = np.zeros([5], dtype=int)
        self.hidden_embedding = np.ones([52], dtype=int)
        self.win_probability = 0.0
        self.draw_probability = 1.0

        if type(hands) != np.ndarray:
            self.hands = np.array(hands, dtype=int)
        else:
            self.hands = hands
        if self.hands.shape[0] == 2:
            for i in range(2):
                self.hidden_embedding[self.hands[i] - 1] = 0
        else:
            exit('Your own hands must be 2...')

    def flop(self, flops):
        if flops and len(flops) == 3:
            if 0 not in flops:
                self.phase = 'flop'
                for i in range(3):
                    self.hidden_embedding[flops[i] - 1] = 0
                    self.table[i] = flops[i]
                win, draw = self.calculate()
                self.win_probability = win
                self.draw_probability = draw
        else:
            exit('Pre-Flops must be 3...')

    def turn(self, turn):
        if turn and len(turn) == 1:
            if turn[0] != 0:
                self.phase = 'turn'
                self.hidden_embedding[turn[0] - 1] = 0
                self.table[3] = turn[0]
                win, draw = self.calculate()
                self.win_probability = win
                self.draw_probability = draw
        else:
            exit('Turn must only be 1...')

    def river(self, river):
        if river and len(river) == 1:
            if river[0] != 0:
                self.phase = 'river'
                self.hidden_embedding[river[0] - 1] = 0
                self.table[4] = river[0]
                win, draw = self.calculate()
                self.win_probability = win
                self.draw_probability = draw
        else:
            exit('River must only be 1...')

    def get_hidden_embedding(self):
        return self.hidden_embedding

    def get_table(self):
        return self.table

    def calculate(self):
        """
        :return: 自己胜率，自己平手
        """
        # 当前是计算有总共有n组合能赢自己得牌，然后n / (total=990) 直接代表对手能赢自己得几率
        # 玩家个数并不会影响自己得胜率 因为是计算所有能赢自己得组合，或者只会影响到对手得胜率
        possible_cards = self.hidden_embedding
        draw_sets, win_sets = 0, 0
        sFlag, sNut = self._set()
        sFlag = self.Nut2Ind[sFlag]
        for i in range(51):
            if possible_cards[i] == 0:
                continue
            for j in range(i + 1, 52):
                if possible_cards[j] == 0:
                    continue
                ret = self.sub_calculate_win_sets([i + 1, j + 1], sFlag, sNut)
                if ret != -1:
                    win_sets += ret
                else:
                    draw_sets += 1

        h_cards = self._get_all_hidden_cards()
        h_ways = h_cards * (h_cards - 1) / 2
        prob = win_sets / h_ways
        draw_prob = draw_sets / h_ways
        win_prob = 1 - draw_prob - prob
        return win_prob, draw_prob

    def sub_calculate_win_sets(self, hands, sFlag, sNut):
        """
        计算对手是否赢，对手赢:1 自己赢:0 平手:0(暂记)
        :param hands:
        :param sFlag:
        :param sNut:
        :return:
        """
        eFlag, eNut = self._set(hands=hands)
        eFlag = self.Nut2Ind[eFlag]
        if sFlag < eFlag:
            return 1
        elif sFlag == eFlag:
            ret = self.compare_same_sets(sNut, eNut, sFlag)
            return ret
        return 0

    def _get_all_hidden_cards(self):
        if self.phase == 'pre-flop':
            return 50
        elif self.phase == 'flop':
            return 47
        elif self.phase == 'turn':
            return 46
        else:
            return 45

    def get_nuts(self):
        return self._set()

    def get_prob(self):
        return self.win_probability, self.draw_probability

    def _set(self, hands=None):
        colors = np.zeros([4], dtype=int)

        if hands is None:
            whole_cards = np.concatenate((self.hands, self.table))
        else:
            whole_cards = np.concatenate((hands, self.table))

        if self.phase == 'flop':
            whole_cards = whole_cards[:-2]
        elif self.phase == 'turn':
            whole_cards = whole_cards[:-1]

        whole_cards = np.sort(whole_cards)

        whole_cards = np.array([i - 1 for i in whole_cards], dtype=int)
        cards = whole_cards.shape[0]
        assert cards >= 5

        for i in range(cards):
            colors[int(whole_cards[i] / 13)] += 1

        flag, nut = self._get_royal_flush(whole_cards=whole_cards, cards=cards)
        if flag:
            return self.Ind2Nut[flag], nut
        flag, nut = self._get_straight_flush(whole_cards=whole_cards, cards=cards)
        if flag:
            return self.Ind2Nut[flag], nut
        flag, nut = self._get_four_of_a_kind(whole_cards=whole_cards)
        if flag:
            return self.Ind2Nut[flag], nut
        flag, nut = self._get_full_house(whole_cards=whole_cards)
        if flag:
            return self.Ind2Nut[flag], nut
        flag, nut = self._get_flush(whole_cards=whole_cards, colors=colors)
        if flag:
            return self.Ind2Nut[flag], nut
        flag, nut = self._get_straight(whole_cards=whole_cards)
        if flag:
            return self.Ind2Nut[flag], nut
        flag, nut = self._get_three_of_a_kind(whole_cards=whole_cards)
        if flag:
            return self.Ind2Nut[flag], nut
        flag, nut = self._get_two_pairs(whole_cards=whole_cards)
        if flag:
            return self.Ind2Nut[flag], nut
        flag, nut = self._get_pair(whole_cards=whole_cards)
        if flag:
            return self.Ind2Nut[flag], nut
        flag, nut = self._get_high_card(whole_cards=whole_cards)
        return self.Ind2Nut[flag], nut

    def _get_royal_flush(self, whole_cards, cards):
        for i in range(cards - 4):
            sets = np.array(
                [[0, 9, 10, 11, 12],
                 [13, 22, 23, 24, 25],
                 [26, 35, 36, 37, 38],
                 [39, 48, 49, 50, 51]]
                , dtype=int)
            width = sets.shape[0]
            for i in range(width):
                if np.intersect1d(sets[i], whole_cards).shape[0] == 5:
                    return 9, np.array([9, 10, 11, 12, 0], dtype=int)
        return 0, np.zeros([5], dtype=int)

    def _get_straight_flush(self, whole_cards, cards):
        midK = [12, 25, 38]
        for i in range(cards - 4):
            head = whole_cards[-(i + 5)]
            tail = whole_cards[-(i + 1)]
            delta = tail - head
            tmparray = whole_cards[-(i + 5): -(i + 1)]
            if delta == 4 and np.intersect1d(midK, tmparray).shape[0] == 0:
                if i == 0:
                    tmparray = whole_cards[-(i + 5):]
                else:
                    tmparray = whole_cards[-(i + 5): -i]
                tmparray = [i % 13 for i in tmparray]
                return 8, np.array(tmparray, dtype=int)
        return 0, np.zeros([5], dtype=int)

    def _get_four_of_a_kind(self, whole_cards, cards=None):
        sortArray = self.return_sorted_true_values(whole_cards)
        fourKind = self.return_same_values(sortArray, 4)
        if fourKind.shape[0] == 0:
            return 0, np.zeros([5], dtype=int)

        high = 1
        for i in sortArray:
            if i != fourKind[0][0]:
                if (i >= high != 0) or i == 0:
                    high = i
        return 7, np.concatenate((fourKind[0], [high]))

    def _get_full_house(self, whole_cards, cards=None):
        sortArray = self.return_sorted_true_values(whole_cards)
        threeKind = self.return_same_values(sortArray, 3)
        pairs = self.return_same_values(sortArray, 2)
        if threeKind.shape[0] == 0 or pairs.shape[0] == 0:
            return 0, np.zeros([5], dtype=int)

        target_three_kind = threeKind[0]
        target_pairs = pairs[0]

        for i in range(1, threeKind.shape[0]):
            if (threeKind[i][0] > target_three_kind[0] != 0) or \
                    threeKind[i][0] == 0:
                target_three_kind = threeKind[i]

        for i in range(1, pairs.shape[0]):
            if (pairs[i][0] > target_pairs[0] != 0) or \
                    pairs[i][0] == 0:
                if pairs[i][0] not in target_three_kind:
                    target_pairs = pairs[i]

        if target_pairs[0] == target_three_kind[0]:
            return 0, np.zeros([5], dtype=int)

        return 6, np.concatenate((target_three_kind, target_pairs))

    def _get_flush(self, whole_cards, colors):
        ret = []
        color, upperK = 0, 0
        for ind in range(len(colors)):
            if colors[ind] >= 5:
                upperK = (ind + 1) * 13 - 1
                color = ind
                break

        if upperK == 0:
            return 0, np.zeros([5], dtype=int)

        for c in whole_cards:
            if int(c / 13) == color:
                ret.append(c % 13)

        # if Ace
        if 0 in ret:
            ret.append(0)
        return 5, np.array(ret[-5:], dtype=int)

    def _get_straight(self, whole_cards, cards=None):
        sortArray = self.return_sorted_true_values(whole_cards)
        # 将排序后的数组(第一个元素 + 13)加到数组最后面，如果是Ace则可以成顺，不是也不影响结果
        # 从后面往前拿，先拿到得就是最大的顺子
        sortArray.append(sortArray[0] + 13)
        tail = len(sortArray) - 1
        for ind in range(tail - 3):
            flag = True
            item = sortArray[tail - ind]
            expected = [item - 4, item - 3, item - 2, item - 1, item]
            for e in expected[:-1]:
                if e not in sortArray:
                    flag = False
                    break
            if flag:
                # if ends with Ace(13), turn 13 back to 0
                if expected[-1] == 13:
                    expected[-1] = 0
                return 4, np.array(expected, dtype=int)
        return 0, np.zeros([5], dtype=int)

    def _get_three_of_a_kind(self, whole_cards, cards=None):
        sortArray = self.return_sorted_true_values(whole_cards)

        threeKind = self.return_same_values(sortArray, 3)
        if threeKind.shape[0] == 0:
            return 0, np.zeros([5], dtype=int)

        target_three_kind = threeKind[0]
        for i in range(1, threeKind.shape[0]):
            if (threeKind[i][0] > target_three_kind[0] != 0) or \
                    threeKind[i][0] == 0:
                target_three_kind = threeKind[i]

        highs = collections.deque(maxlen=2)
        for item in sortArray:
            if item not in target_three_kind:
                highs.append(item)
        # if Ace
        if 0 in sortArray and 0 not in target_three_kind:
            highs.append(0)

        return 3, np.concatenate((target_three_kind, highs))

    def _get_two_pairs(self, whole_cards, cards=None):
        sortArray = self.return_sorted_true_values(whole_cards)
        twoPairs = self.return_same_values(sortArray, 2)
        if twoPairs.shape[0] < 2:
            return 0, np.zeros([5], dtype=int)

        twoHighPairs = twoPairs[-2:]
        if twoPairs.shape[0] == 3 and twoPairs[0][0] == 0:
            twoHighPairs[0] = twoPairs[0]

        targetHigh = 1
        pairCards = [twoHighPairs[0][0], twoHighPairs[1][0]]
        for item in sortArray:
            if item not in pairCards:
                if (item > targetHigh != 0) or item == 0:
                    targetHigh = item

        return 2, np.concatenate((twoHighPairs[0], twoHighPairs[1], [targetHigh]))

    def _get_pair(self, whole_cards, cards=None):
        sortArray = self.return_sorted_true_values(whole_cards)
        pairs = self.return_same_values(sortArray, 2)
        if pairs.shape[0] < 1:
            return 0, np.zeros([5], dtype=int)

        assert pairs.shape[0] == 1

        highs = collections.deque(maxlen=3)
        for item in sortArray:
            if item != pairs[0][0]:
                highs.append(item)
        # if Ace
        if 0 in sortArray and 0 not in pairs[0]:
            highs.append(0)

        return 1, np.concatenate((pairs[0], highs))

    def _get_high_card(self, whole_cards, cards=None):
        sortArray = self.return_sorted_true_values(whole_cards)
        highs = collections.deque(iterable=sortArray[-5:], maxlen=5)
        if 0 in sortArray and 0 not in highs:
            highs.append(0)

        return 0, np.array(highs, dtype=int)

    def return_same_values(self, arr, times):
        """
        :param arr: 处理的数组
        :param times: 要求重复次数
        :return: shape[n, times]
        """
        arr = np.sort(arr)
        width = arr.shape[0]
        ret = []
        for i in range(width):
            if i + times <= width:
                tmp = arr[i: i + times]
                tmp = [i for i in tmp if i == tmp[0]]
                if len(tmp) == times and tmp not in ret:
                    ret.append(tmp)
            else:
                break
        if ret:
            return np.array(ret, dtype=int)
        return np.array([])

    def return_sorted_true_values(self, array):
        tmparray = [i % 13 for i in array]
        tmparray = sorted(tmparray)
        return tmparray

    def compare_same_sets(self, set1, set2, flag):
        """
        相同组合下哪一个组合赢
        :param set1:
        :param set2:
        :param flag:
        :return:int: 0->set1 wins, 1->set2 wins, -1->draw
        """
        ind = [i for i in range(13)]
        val = [13]
        val.extend(ind[1:])
        true_values = dict(zip(ind, val))
        if flag == 9:
            return -1
        elif flag == 8:
            if set1[4] == set2[4]:
                return -1
            elif set1[4] > set2[4]:
                return 0
            else:
                return 1
        elif flag == 7:
            v1 = true_values[set1[0]]
            v2 = true_values[set2[0]]
            return 0 if v1 > v2 else 1
        elif flag == 6:
            three1 = true_values[set1[0]]
            three2 = true_values[set2[0]]
            if three1 != three2:
                return 0 if three1 > three2 else 1

            pair1 = true_values[set1[3]]
            pair2 = true_values[set2[3]]
            if pair1 != pair2:
                return 0 if pair1 > pair2 else 1
            return -1
        elif flag == 5:
            v1 = [true_values[i] for i in set1]
            v2 = [true_values[i] for i in set2]
            for i in range(len(v1)):
                if v1[i] != v2[i]:
                    return 0 if v1[i] > v2[i] else 1
            return -1
        elif flag == 4:
            v1 = true_values[set1[0]]
            v2 = true_values[set2[0]]
            if v1 != v2:
                return 0 if v1 > v2 else 1
            return -1
        elif flag == 3:
            three1 = true_values[set1[0]]
            three2 = true_values[set2[0]]
            if three1 != three2:
                return 0 if three1 > three2 else 1

            high1 = sorted([true_values[set1[3]], true_values[set1[4]]], reverse=True)
            high2 = sorted([true_values[set2[3]], true_values[set2[4]]], reverse=True)
            for i in range(len(high1)):
                if high1[i] != high2[i]:
                    return 0 if high1[i] > high2[i] else 1
            return -1
        elif flag == 2:
            v1 = sorted([true_values[set1[0]], true_values[set1[2]], true_values[set1[4]]], reverse=True)
            v2 = sorted([true_values[set1[0]], true_values[set1[2]], true_values[set1[4]]], reverse=True)
            for i in range(len(v1)):
                if v1[i] != v2[i]:
                    return 0 if v1[i] > v2[i] else 1
            return -1
        elif flag == 1:
            v1 = sorted([true_values[set1[0]], true_values[set1[2]], true_values[set1[3]], true_values[set1[4]]],
                        reverse=True)
            v2 = sorted([true_values[set1[0]], true_values[set1[2]], true_values[set1[3]], true_values[set1[4]]],
                        reverse=True)
            for i in range(len(v1)):
                if v1[i] != v2[i]:
                    return 0 if v1[i] > v2[i] else 1
            return -1
        else:
            v1 = sorted([true_values[i] for i in set1], reverse=True)
            v2 = sorted([true_values[i] for i in set2], reverse=True)
            for i in range(len(v1)):
                if v1[i] != v2[i]:
                    return 0 if v1[i] > v2[i] else 1
            return -1


def get_poker_table_instance(hands, pre_flop, turn, river):
    pokerTable = PokerTable(hands=hands)
    pokerTable.flop(flops=pre_flop)
    pokerTable.turn(turn=turn)
    pokerTable.river(river=river)
    return pokerTable


if __name__ == '__main__':
    hands = [14, 16]
    flop = [5, 20, 21]
    turn = [42]
    river = [26]
    pt = get_poker_table_instance(hands, flop, turn, river)
    f, n = pt.get_nuts()

    print(f, n)
    print(pt.calculate())

