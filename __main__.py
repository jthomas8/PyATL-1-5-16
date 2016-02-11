#!/usr/local/bin/python3

import numpy as np
from scipy import stats
import csv

def hand_value(values, suits):
    if(values.max() == 4):
        return 19, '4 of a kind'
    if((suits.max() == 5) & (np.trim_zeros(values).__len__() != 5)):
        return 17, 'flush'
    if(values.max() == 3):
        if(np.any(values == 2)):
            return 18, 'full house'
        else:
            return 15, '3 of a kind'
    if(values.max() == 2):
        if(stats.mode(values) == 2):
            return 15, '2 pairs'
        else:
            return 13, '2 of a kind'
    if(np.trim_zeros(values).__len__() == 5):
        if(suits.max() == 5):
            return 20, 'straight flush'
        else:
            return 16, 'straight'
    return str(np.trim_zeros(values, 'b').__len__()), 'high card: ' + str(np.trim_zeros(values, 'b').__len__())

def compare_hand(hand1, hand2):
    hand1_value, hand2_value = 0, 0;
    suits1, suits2 = (hand1.sum(axis=0), hand2.sum(axis=0))
    values1, values2 = (hand1.sum(axis=1), hand2.sum(axis=1))
    
    hand1_value, hand1_name = hand_value(values1, suits1)
    hand2_value, hand2_name = hand_value(values2, suits2)
    print(hand1_name)
    print(hand2_name)
    if(hand1_value > hand2_value):
        print('Black wins. - with ' + hand1_name)
    elif(hand2_value > hand1_value):
        print('White wins. - with ' + hand2_name)
    else:
        print('Tie. still needs to be broken')

def get_card_val(card_string):

    value = np.zeros(13, dtype=int)
    suit = np.zeros(4, dtype=int)
    card_val = card_string[0:-1]
    if(card_val == 'A'):
        np.put(value, 12, 1)
    elif(card_val == 'K'):
        np.put(value, 11, 1)
    elif(card_val == 'Q'):
        np.put(value, 10, 1)
    elif(card_val == 'J'):
        np.put(value, 9, 1)
    else:
        np.put(value, int(card_val)-2, 1)

    if(card_string[-1] == 'S'):
        np.put(suit, 3, 1)
    elif(card_string[-1] == 'H'):
        np.put(suit, 2, 1)
    elif(card_string[-1] == 'D'):
        np.put(suit, 1, 1)
    elif(card_string[-1] == 'C'):
        np.put(suit, 0, 1)
    value = np.matrix(value)
    value = value.T
    value, suit = np.broadcast_arrays(value, suit)
    return value * suit

bhands = np.zeros(shape=(13,4,5), dtype=int)
whands = np.zeros(shape=(13,4,5), dtype=int)
bhlist, whlist = [], []
results = []
with open('test.txt', newline='\n') as testcases:
    results = []
    for line in csv.reader(testcases):
        results.append(line)
    for hand in results:
        bhlist.append(hand[0].strip('Black: ').split('  White: ')[0].split(' '))
        whlist.append(hand[0].strip('Black: ').split('  White: ')[1].split(' '))

for i in np.arange(bhlist.__len__()):
    black_hand, white_hand = (bhlist[i], whlist[i])
    black_temp, white_temp = (np.zeros(shape=(13,4), dtype=int), np.zeros(shape=(13,4), dtype=int))
    for j in np.arange(black_hand.__len__()):
        black_card, white_card = black_hand[j], white_hand[j]
        black_temp += get_card_val(black_card)
        white_temp += get_card_val(white_card)
    bhands[:,:,i],whands[:,:,i] = black_temp, white_temp

compare_hand(bhands[:,:,2], whands[:,:,2])
#print(bhands[:,:,0])
#print(bhlist)
#print(whlist)
