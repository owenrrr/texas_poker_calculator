#!/usr/bin/env python 
# -*- coding:utf-8 -*-
import PySimpleGUI as sg
import poker_table as pt


def viewer():
    sg.theme('DarkAmber')
    default_color = 'white'
    texts = ['', '', '', '', '', '', '']
    Flowers = ['Club', 'Diamond', 'Heart', 'Spade']
    Number = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    Num2Ind = dict(zip(Number, [i for i in range(1, 14)]))
    Ind2Number = dict(zip([i for i in range(13)], Number))

    hands = [0, 0]
    preFlop = [0, 0, 0]
    turn = [0]
    river = [0]

    layout = [
              [
                  sg.Frame(layout=[
                      [sg.Text('Card 1:', text_color=default_color),
                       sg.ButtonMenu(button_text='Club', menu_def=[[], Number]),
                       sg.ButtonMenu(button_text='Diamond', menu_def=[[], Number]),
                       sg.ButtonMenu(button_text='Heart', menu_def=[[], Number]),
                       sg.ButtonMenu(button_text='Spade', menu_def=[[], Number]),
                       sg.Text(texts[0], key='_card_one_', text_color=default_color)],
                      [sg.Text('Card 2:', text_color=default_color),
                       sg.ButtonMenu(button_text='Club', menu_def=[[], Number]),
                       sg.ButtonMenu(button_text='Diamond', menu_def=[[], Number]),
                       sg.ButtonMenu(button_text='Heart', menu_def=[[], Number]),
                       sg.ButtonMenu(button_text='Spade', menu_def=[[], Number]),
                       sg.Text(texts[1], key='_card_two_', text_color=default_color)]
                  ], title='Hand Cards', border_width=5)
              ],
              [
                  sg.Frame(layout=[
                      [sg.Text('Flop 1:', text_color=default_color),
                       sg.ButtonMenu(button_text='Club', menu_def=[[], Number]),
                       sg.ButtonMenu(button_text='Diamond', menu_def=[[], Number]),
                       sg.ButtonMenu(button_text='Heart', menu_def=[[], Number]),
                       sg.ButtonMenu(button_text='Spade', menu_def=[[], Number]),
                       sg.Text(texts[2], key='_preflop_one_', text_color=default_color)],
                      [sg.Text('Flop 2:', text_color=default_color),
                       sg.ButtonMenu(button_text='Club', menu_def=[[], Number]),
                       sg.ButtonMenu(button_text='Diamond', menu_def=[[], Number]),
                       sg.ButtonMenu(button_text='Heart', menu_def=[[], Number]),
                       sg.ButtonMenu(button_text='Spade', menu_def=[[], Number]),
                       sg.Text(texts[3], key='_preflop_two_', text_color=default_color)],
                      [sg.Text('Flop 3:', text_color=default_color),
                       sg.ButtonMenu(button_text='Club', menu_def=[[], Number]),
                       sg.ButtonMenu(button_text='Diamond', menu_def=[[], Number]),
                       sg.ButtonMenu(button_text='Heart', menu_def=[[], Number]),
                       sg.ButtonMenu(button_text='Spade', menu_def=[[], Number]),
                       sg.Text(texts[4], key='_preflop_three_', text_color=default_color)]
                  ], title='Flops', border_width=5)
              ],
              [
                    sg.Frame(layout=[
                        [sg.Text('Turn:', text_color=default_color),
                        sg.ButtonMenu(button_text='Club', menu_def=[[], Number]),
                        sg.ButtonMenu(button_text='Diamond', menu_def=[[], Number]),
                        sg.ButtonMenu(button_text='Heart', menu_def=[[], Number]),
                        sg.ButtonMenu(button_text='Spade', menu_def=[[], Number]),
                        sg.Text(texts[5], key='_turn_', text_color=default_color)]
                    ], title='The Turn', border_width=5)
              ],
              [
                    sg.Frame(layout=[
                        [sg.Text('River:', text_color=default_color),
                        sg.ButtonMenu(button_text='Club', menu_def=[[], Number]),
                        sg.ButtonMenu(button_text='Diamond', menu_def=[[], Number]),
                        sg.ButtonMenu(button_text='Heart', menu_def=[[], Number]),
                        sg.ButtonMenu(button_text='Spade', menu_def=[[], Number]),
                        sg.Text(texts[6], key='_river_', text_color=default_color)]
                    ], title='The River', border_width=5)
              ],
              [
                  sg.Text(' ' * 20),
                  sg.Text('', key='_nut_',font=10, text_color=default_color),
                  sg.Text('', key='_nut_cards_', font=100, text_color=default_color)
              ],
              [
                  sg.Text(' ' * 20),
                  sg.Text('', key='_win_prob_', font=100, text_color='green'),
              ],
              [
                  sg.Text(' ' * 20),
                  sg.Text('', key='_draw_prob_', font=100, text_color='red')
              ],
              [sg.Text('\n')],
              [
                  sg.Button('Calculate'),
                  sg.Text(' ' * 80),
                  sg.Button('Refresh')
              ],
            ]

    window = sg.Window('Texas Poker', layout=layout, size=(500, 500))

    mask = [0] * 7

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED:
            break

        # change text
        if type(event) == int:
            if 0 <= event <= 3:
                t1, t2 = texts[0], hands[0]
                texts[0] = Flowers[event % 4] + ' ' + values[event]
                hands[0] = (event % 4) * 13 + Num2Ind[values[event]]
                if False in check_duplicate(hands, preFlop, turn, river):
                    sg.popup_timed('Duplicate Card exists...Please Check!')
                    texts[0], hands[0] = t1, t2
                else:
                    window.find_element(key='_card_one_').update(texts[0])
                    mask[0] = 1
            elif 4 <= event <= 7:
                t1, t2 = texts[1], hands[1]
                texts[1] = Flowers[event % 4] + ' ' + values[event]
                hands[1] = (event % 4) * 13 + Num2Ind[values[event]]
                ret = check_duplicate(hands, preFlop, turn, river)
                if False in check_duplicate(hands, preFlop, turn, river):
                    sg.popup_timed('Duplicate Card exists...Please Check!')
                    texts[1], hands[1] = t1, t2
                else:
                    window.find_element(key='_card_two_').update(texts[1])
                    mask[1] = 1
            elif 8 <= event <= 11:
                t1, t2 = texts[2], preFlop[0]
                texts[2] = Flowers[event % 4] + ' ' + values[event]
                preFlop[0] = (event % 4) * 13 + Num2Ind[values[event]]
                if False in check_duplicate(hands, preFlop, turn, river):
                    sg.popup_timed('Duplicate Card exists...Please Check!')
                    texts[2], preFlop[0] = t1, t2
                else:
                    window.find_element(key='_preflop_one_').update(texts[2])
                    mask[2] = 1
            elif 12 <= event <= 15:
                t1, t2 = texts[3], preFlop[1]
                texts[3] = Flowers[event % 4] + ' ' + values[event]
                preFlop[1] = (event % 4) * 13 + Num2Ind[values[event]]
                if False in check_duplicate(hands, preFlop, turn, river):
                    sg.popup_timed('Duplicate Card exists...Please Check!')
                    texts[3], preFlop[1] = t1, t2
                else:
                    window.find_element(key='_preflop_two_').update(texts[3])
                    mask[3] = 1
            elif 16 <= event <= 19:
                t1, t2 = texts[4], preFlop[2]
                texts[4] = Flowers[event % 4] + ' ' + values[event]
                preFlop[2] = (event % 4) * 13 + Num2Ind[values[event]]
                if False in check_duplicate(hands, preFlop, turn, river):
                    sg.popup_timed('Duplicate Card exists...Please Check!')
                    texts[4], preFlop[2] = t1, t2
                else:
                    window.find_element(key='_preflop_three_').update(texts[4])
                    mask[4] = 1
            elif 20 <= event <= 23:
                t1, t2 = texts[5], turn[0]
                texts[5] = Flowers[event % 4] + ' ' + values[event]
                turn[0] = (event % 4) * 13 + Num2Ind[values[event]]
                if False in check_duplicate(hands, preFlop, turn, river):
                    sg.popup_timed('Duplicate Card exists...Please Check!')
                    texts[5], turn[0] = t1, t2
                else:
                    window.find_element(key='_turn_').update(texts[5])
                    mask[5] = 1
            elif 24 <= event <= 27:
                t1, t2 = texts[6], river[0]
                texts[6] = Flowers[event % 4] + ' ' + values[event]
                river[0] = (event % 4) * 13 + Num2Ind[values[event]]
                if False in check_duplicate(hands, preFlop, turn, river):
                    sg.popup_timed('Duplicate Card exists...Please Check!')
                    texts[6], river[0] = t1, t2
                else:
                    window.find_element(key='_river_').update(texts[6])
                    mask[6] = 1

        if event == 'Calculate':
            if find_ones(mask) >= 5:
                nut, set, win, draw = get_all_results(hands, preFlop, turn, river)
                set = [Ind2Number[item] for item in set]
                window.find_element(key='_nut_').update(nut)
                window.find_element(key='_nut_cards_').update(set)
                win_text = "Winning Rate：%.4f" % (win * 100)
                draw_text = "Draw Rate：%.4f" % (draw * 100)
                window.find_element(key='_win_prob_').update(win_text + '%')
                window.find_element(key='_draw_prob_').update(draw_text + '%')
                print(hands, preFlop, turn, river)
                print('win:', win, '; draw', draw)

        if event == 'Refresh':
            window.find_element(key='_card_one_').update('')
            window.find_element(key='_card_two_').update('')
            window.find_element(key='_preflop_one_').update('')
            window.find_element(key='_preflop_two_').update('')
            window.find_element(key='_preflop_three_').update('')
            window.find_element(key='_turn_').update('')
            window.find_element(key='_river_').update('')
            window.find_element(key='_nut_').update('')
            window.find_element(key='_nut_cards_').update('')
            window.find_element(key='_win_prob_').update('')
            window.find_element(key='_draw_prob_').update('')
            mask = [0] * 7

    window.close()


def get_set(hands, pre_flop, turn, river):
    pokerTable = pt.PokerTable(hands=hands)
    pokerTable.flop(flops=pre_flop)
    pokerTable.turn(turn=turn)
    pokerTable.river(river=river)

    flag, set = pokerTable._set()
    return flag, set


def get_all_results(hands, pre_flop, turn, river):
    pokerTable = pt.PokerTable(hands=hands)
    pokerTable.flop(flops=pre_flop)
    pokerTable.turn(turn=turn)
    pokerTable.river(river=river)

    flag, set = pokerTable.get_nuts()
    win, draw = pokerTable.get_prob()
    return flag, set, win, draw


def find_ones(arr):
    if len(arr) != 7:
        return -1
    times = 0
    for i in arr:
        if i == 1:
            times += 1
        else:
            break
    return times


def check_duplicate(hands, pre_flop=[], turn=[], river=[]):
    # assert hands length must be at least 2
    assert len(hands) == 2
    # ret = [hands, pre-flop, hands x pre-flop, hands x turn,
    # hands x river, pre-flop x turn, pre-flop x river, turn x river]
    ret = [True] * 8
    if hands[0] == hands[1] and hands[0] != 0:
        ret[0] = False
    if len(pre_flop) == 3:
        if (pre_flop[0] == pre_flop[1] and pre_flop[0] != 0) or \
                (pre_flop[0] == pre_flop[2] and pre_flop[0] != 0) or \
                (pre_flop[1] == pre_flop[2] and pre_flop[1] != 0):
            ret[1] = False
        for item in hands:
            if item in pre_flop and item != 0:
                ret[2] = False
    if len(turn) and turn[0] in hands and turn[0] != 0:
        ret[3] = False
    if len(river) and river[0] in hands and river[0] != 0:
        ret[4] = False
    if len(turn) and turn[0] in pre_flop and turn[0] != 0:
        ret[5] = False
    if len(river) and river[0] in pre_flop and river[0] != 0:
        ret[6] = False
    if len(turn) and len(river) and turn[0] == river[0] and turn[0] != 0:
        ret[7] = False

    return ret


if __name__ == '__main__':
    viewer()
