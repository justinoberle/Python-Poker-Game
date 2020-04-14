# -*- coding: utf-8 -*-
"""
Created on Sun Apr  5 19:09:22 2020

@author: justinoberle
"""

''' Create a plot of each persons winning whole cards and count each one. There are 2 ways to do this.
    One is simply counting all occurances of a win but this will NOT account for hands that are less
    common. The better way to do this is might be to count number of times this hand was an option
    vs number of times it actually won. Do this first one first though '''

import poker
import time
from collections import Counter
import matplotlib.pyplot as plt
from itertools import combinations

players = 5      
iterations = 10000       
                     
#whole_cards, flop, turn, river, com_cards = poker.BestHand.full_game_dealt(10, poker.full_deck)
#poker.BestHand.find_best_hand(whole_cards, flop, turn, river, com_cards)
#print('\n###', com_cards, '###\n')
#print('---', whole_cards, '---\n')
#print('--------------------------------------------------')

def poker_debug(iterations):
    for i in range(iterations):
        whole_cards, flop, turn, river, com_cards = poker.BestHand.full_game_dealt(10, poker.full_deck)
        poker.BestHand.find_best_hand(whole_cards, flop, turn, river, com_cards)
#        print('\n###', com_cards, '###\n')
#        print('---', whole_cards, '---\n')
#        print('--------------------------------------------------')

class Statistics:

    def percent_hand_type_wins(players, iterations, optimize=False):
        # This verifies that poker logic is working in poker.py by comparing to actual probabilities.
        
        j = 0
        while j < players:
            t1 = time.time()
            counts = []
            if optimize == True:
                iterate = int(iterations / (j+1))
            else:
                iterate = iterations
            for i in range(iterate):
                whole_cards, flop, turn, river, com_cards = poker.BestHand.full_game_dealt(j+1, poker.full_deck)
                counts.append(poker.BestHand.find_best_hand(whole_cards, flop, turn, river, com_cards, 
                                                            count=True, best_player_bool=False))
            print(time.time() - t1)
                
            full_count = Counter(counts).most_common()
            x = [full_count[i][0] for i, x in enumerate(full_count)]
            y = [(full_count[i][1] / iterate) * 100 for i, x in enumerate(full_count)]
            plt.figure("Best Hands", figsize=(8,4))
            plt.scatter(x, y, label=('Number of players: ' + str(j+1)))
            
            j += 1
#        actual = [43.8, 23.5, 17.4, 4.83, 4.62, 3.03, 2.6, .168, .0279]
#        plt.scatter(x, actual, label=("Actual Probability"))
        plt.legend()
        plt.title("Percentage each hand is won with (x) players in " + str(iterations) + " iterations")
        plt.xlabel("Hands")
        plt.ylabel("Winning Percentage")    


   
# first need to find the winning whole cards for a given hand. Then put it in loop and append winners
winning_hands = []
draw_hands = []
winning_hand_types = []
winning_hand_numbers = []
winning_hand_suits = []
for i in range(10000):
    whole_cards, flop, turn, river, com_cards = poker.BestHand.full_game_dealt(10, poker.full_deck)
    player_number, player_hand = poker.BestHand.find_best_hand(whole_cards, flop, turn, river, com_cards, 
                                                count=False, best_player_bool=True)
#    print('\n###', com_cards, '###\n')
#    print('---', whole_cards, '---\n')
#    print('--------------------------------------------------')
    
    if len(player_number) == 1:
        winner = whole_cards[player_number[0] - 1]
        winning_hands.append(winner)
        winning_hand_types.append(player_hand)
        winning_hand_numbers.append(poker.Hands.hand_numbers(poker.Hands.preflop_hands([winner]), winner))
        winning_hand_suits.append(poker.Hands.hand_suits(poker.Hands.preflop_hands([winner]), winner))
    
    elif len(player_number) > 1:
        for i in range(len(player_number)):
            draw_hands.append(whole_cards[player_number[i] - 1])
    else:
        print('WTF!!!!!!!!!!!!!!!!!!!!!!!!!!!')


# create, numbers, suits_bool, and winning_hand_types to categorize everything
numbers = [j for sub in winning_hand_numbers for j in sub]
suits = [j for sub in winning_hand_suits for j in sub]
suits_bool = []
for i in range(len(suits)):
    if suits[i][0] == suits[i][1]:
        suits_bool.append(True)
    else:
        suits_bool.append(False)

# creatd 91 index values for each combination and found the index location of each hand.
list1 = [1,2,3,4,5,6,7,8,9,10,11,12,13]
combos = [items for items in combinations(list1, r=2)]
for i in range(1, 14):
    combos.append((i, i))
combos_index = []
for x in numbers:
    x = tuple(sorted(x))
    for i in combos:
        if x == i:
            combos_index.append(combos.index(i))
        else:
            pass

# now we can use Counter on the indexes and then convert the indexes back to lists(hands)
index_counter = Counter(combos_index)
most_common = index_counter.most_common()

# need to iterate through most common and above 77 needs to be multiplied by 2 for probablity adjustment.
common = [list(i) for i in most_common]
for i in range(len(common)):
    if common[i][0] > 77:
        common[i][1] *= 2
    else:
        pass
sorted_common = sorted(common, key=lambda x: x[1], reverse=True)

# convert indexes back to hands using combos as reference
actual = []
for i in range(len(sorted_common)):
    index = sorted_common[i][0]
    actual.append([combos[index], sorted_common[i][1]])
        
        



