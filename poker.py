# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 21:42:01 2020

@author: justinoberle
"""
''' debug then find bottlenecks'''
''' 1) improved from 13 to 3 second runtime of 10 000 iterations for best_hand() by moving the 
    Hands.hand_numbers() and Hands.hand_suits() functions to only unpack at the beginning
    and not every single check for a hand'''
''' 2) try improve the Hands.hand_numbers() and Hands.hand_suits() functions to optimize '''
''' Try to make a poker game '''
''' try to make a computer win a lot '''
''' found some bugs in straight and one pair. one pair was evaluating all 7 cards for high card
    instead of remaining 3. straight might need more checks.'''

import numpy as np
from collections import Counter
import random
import time
import matplotlib.pyplot as plt


#deck = ['xA', 'x2', 'x3', 'x4', '10']
#deck = ['xA', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', '10', 'xJ', 'xQ', 'xK', '15', '16',
#        '17', '18', '19', '20']
deck = ['xA', 'x2', 'x3', 'x4', 'x5', 'x6', 'x7', 'x8', 'x9', '10', 'xJ', 'xQ', 'xK']

deck_suits = ['Spade', 'Heart', 'Club', 'Diamond']

full_deck = [i+j for i in deck for j in deck_suits]
        
class GameLogic:
    
    def sort_2d_array(darray):
        sorted_array = []
        for i in range(len(darray)):
            sorted_array.append(sorted(darray[i]))
        return sorted_array
    
    def fourteens_for_aces(array):
        # Make 1's 14's for A's
        array_temp = []
        for i in range(len(array)):
            array_temp.append([14 if x==1 else x for x in array[i]])
        return array_temp
        
    def nan_checker(numbers_list, is2d=True):
        # end function below if all nan values, meaning no players have 2 pair.
        if is2d == True:
            nan_checker = []
            for i in range(len(numbers_list)):
                for j in range(1):
                    if np.isnan(numbers_list[i][j]) == True:
                        pass
                    else:
                        nan_checker.append(numbers_list[i][j])
            if len(nan_checker) == 0:
                return True
            else:
                return False
        # for 1d array
        else:
            nan_checker = []
            for i in range(len(numbers_list)):
                if np.isnan(numbers_list[i]) == True:
                    pass
                else:
                    nan_checker.append(numbers_list[i])
            if len(nan_checker) == 0:
                return True
            else:
                return False
    
    
    def create_list_of_last(sorted_array):
        temp = []
        for ii in range(len(sorted_array)):
            temp.append(sorted_array[ii][-1])
        return temp
    
    def find_highest_card_array(array):
        sorted_array = GameLogic.sort_2d_array(array)
        indices = []
        for i in range(len(sorted_array)):
            indices.append(i)
        for j in range(len(sorted_array[0])):
            temp = GameLogic.create_list_of_last(sorted_array)
            k = 0
            while k < len(temp):
                if temp[k] == np.nanmax(temp):
                    sorted_array[k] = sorted_array[k][:-1]
                    k += 1
                else:
                    if k < len(sorted_array):
                        del sorted_array[k]
                        del indices[k]
                        del temp[k]
                    else:
                        break
                    
            if len(indices) == 1:
                break
                
            else:
                pass
        
        best_player = [i + 1 for i in indices]
        return best_player

class Hands:
        
    def single_hand(whole_cards, flop, turn, river):
        com_cards = flop + [turn] + [river]
        my_hand = list(whole_cards) + com_cards
        return my_hand
    
    def preflop_hands(whole_cards):
        preflop_hands = []
        for i in range(len(whole_cards)):
            preflop_hands.append(list(whole_cards[i]))
        return preflop_hands
    
    def all_hands(whole_cards, flop, turn, river):
        com_cards = flop + [turn] + [river]
        all_hands = []
        for i in range(len(whole_cards)):
            all_hands.append(list(whole_cards[i]) + com_cards)
        return all_hands
      
    def hand_numbers(function, whole_cards, flop=0, turn=0, river=0):
        #for all 7 cards function needs to be Hands.all_hands(whole_cards, flop, turn, river)
        hand_numbers = []
        for i in range(len(function)):
            each_hand_numbers = []
            for j in range(len(function[i])):
                if function[i][j][0:2] == 'xJ':
                    dummy = str(function[i][j][0:2].replace('xJ', '11'))
                elif function[i][j][0:2] == 'xQ':
                    dummy = str(function[i][j][0:2].replace('xQ', '12'))
                elif function[i][j][0:2] == 'xK':
                    dummy = str(function[i][j][0:2].replace('xK', '13'))
                elif function[i][j][0:2] == 'xA':
                    dummy = str(function[i][j][0:2].replace('xA', '01'))
                else:
                    dummy = str(function[i][j][0:2].replace('x', '0'))
                
                each_hand_numbers.append(int(dummy))
            hand_numbers.append(each_hand_numbers)
        return hand_numbers
    
    def hand_suits(function, whole_cards, flop=0, turn=0, river=0):
        #for all 7 cards function needs to be Hands.all_hands(whole_cards, flop, turn, river)
        hand_suits = []
        for i in range(len(function)):
            each_hand_suit = []
            for j in range(len(function[i])):
                if function[i][j][2:] == 'Spade':
                    dummy = str(function[i][j][2:].replace('Spade', '21'))
                elif function[i][j][2:] == 'Club':
                    dummy = str(function[i][j][2:].replace('Club', '22'))
                elif function[i][j][2:] == 'Heart':
                    dummy = str(function[i][j][2:].replace('Heart', '23'))
                elif function[i][j][2:] == 'Diamond':
                    dummy = str(function[i][j][2:].replace('Diamond', '24'))
                else:
                    dummy = str(function[i][j][0:2].replace('x', '0'))
                
                each_hand_suit.append(int(dummy))
            hand_suits.append(each_hand_suit)
        return hand_suits
    '''-------------------------------------------------------------------------------------'''
    ''' ---------------------------------------HIGH HAND------------------------------------'''
    '''-------------------------------------------------------------------------------------'''

    def high_cards(hand_numbers):
        high_card_hand = hand_numbers
        # Make 1's, 14's for A's
        high_card_hand_temp = []
        for i in range(len(high_card_hand)):
            high_card_hand_temp.append([14 if x==1 else x for x in high_card_hand[i]])
        high_card_hand = high_card_hand_temp
        ## Calculate best 5 high cards for each hand
        all_hands = []
        for i in range(len(high_card_hand)):
            temp = sorted(high_card_hand[i])
            best_five = temp[-5:]
            all_hands.append(best_five)
        #find max element in first array, specify how many arrays to do this for. compare max's and remove. iterate again.
        best_player = GameLogic.find_highest_card_array(all_hands)
        return best_player

    
    '''-------------------------------------------------------------------------------------'''
    ''' ---------------------------------------ONE PAIR-------------------------------------'''
    '''-------------------------------------------------------------------------------------'''
        
    def one_pair(hand_numbers):
        
        # find all players with 1 pair
        one_pair_hand = hand_numbers
        # Make 1's, 14's for A's
        array = GameLogic.fourteens_for_aces(one_pair_hand)
        
        # finds all of the players with 1 or more pairs
        player = []
        all_pairs = []
        for i in range(len(array)):
            counter = Counter(array[i])
            if counter.most_common()[0][1] >= 2:
                player.append(i+1)
                pairs = []
                for j in range(len(counter.most_common())):
                    if counter.most_common()[j][1] >= 2:
                        pairs.append(counter.most_common()[j][0])
                    else:
                        pass
                    
                if len(pairs) > 1:
                    pairs = sorted(pairs)
                    pairs = pairs[-1:]
                    for j in range(len(pairs)):
                        array[i].remove(pairs[j])
                        array[i].remove(pairs[j])
                else:
                    for j in range(len(pairs)):
                        array[i].remove(pairs[j])
                        array[i].remove(pairs[j])
                
                all_pairs.append(pairs)
            else:
                pass
        # end function below if all nan values, meaning no players have 2 pair.
        if GameLogic.nan_checker(all_pairs) == True:
            return [None]
        
        # find player with the largest top pair, remove all others
        best_player = []
        indices = []
        for i in range(len(all_pairs)):
            if all_pairs[i] == max(all_pairs):
                best_player.append(player[i])
            else:
                pass
        if len(best_player) == 1:
            return best_player
        
        # find remaining high cards, pick highest. if more than 1 it is a draw. return list always
        indices = [i - 1 for i in best_player]
        new_array = []
        for i in range(len(array)):
            if i in indices:
                sorted_array = sorted(array[i])
                new_array.append(sorted_array[2:])
        best_index = GameLogic.find_highest_card_array(new_array)
        
        best_index = [i - 1 for i in best_index]
        best_player_new = []
        for i in range(len(best_index)):
            best_player_new.append(best_player[best_index[i]])
        return best_player_new
                
    '''-------------------------------------------------------------------------------------'''
    ''' ---------------------------------------TWO PAIR-------------------------------------'''
    '''-------------------------------------------------------------------------------------'''
    
    def two_pair(hand_numbers):
        array = hand_numbers
        # Make 1's, 14's for A's
        array = GameLogic.fourteens_for_aces(array)
        
        # finds all of the players with 2 or more pairs
        player = []
        all_pairs = []
        for i in range(len(array)):
            counter = Counter(array[i])
            if counter.most_common()[0][1] >= 2 and counter.most_common()[1][1] >= 2:
                player.append(i+1)
                pairs = []
                for j in range(len(counter.most_common())):
                    # needs more logic for 3 pair finding 2 highest and not removing 3rd.
                    if counter.most_common()[j][1] >= 2:
                        pairs.append(counter.most_common()[j][0])
                    else:
                        pass
                    
                if len(pairs) > 2:
                    pairs = sorted(pairs)
                    pairs = pairs[-2:]
                    for j in range(len(pairs)):
                        array[i].remove(pairs[j])
                        array[i].remove(pairs[j])
                else:
                    for j in range(len(pairs)):
                        array[i].remove(pairs[j])
                        array[i].remove(pairs[j])

                all_pairs.append(pairs)
            else:
                pass
            
        # end function below if all nan values, meaning no players have 2 pair.
        if GameLogic.nan_checker(all_pairs) == True:
            return [None]
        
        # get only top 2 pair for each player
        indices = [i - 1 for i in player]
        top_two = []
        for i in range(len(all_pairs)):
            temp = sorted(all_pairs[i])
            top_two.append(temp[-2:])
        top_pair = [max(i) for i in top_two]
        bottom_pair = [min(i) for i in top_two]
        # find player with the largest top pair, remove all others
        best_player = []
        new_bottom_pair = []
        for i in range(len(top_pair)):
            if top_pair[i] == max(top_pair):
                best_player.append(player[i])
                new_bottom_pair.append(bottom_pair[i])
            else:
                pass
        if len(best_player) == 1:
            return best_player
        
        # find player with best bottom pair, remove all others
        best_bottom = []
        for i in range(len(new_bottom_pair)):
            if new_bottom_pair[i] == max(new_bottom_pair):
                best_bottom.append(best_player[i])
            else:
                pass
        best_player = best_bottom
        if len(best_player) == 1:
            return best_player
        
        # find remaining high card, pick highest. if more than 1 it is a draw. return list always
        indices = [i - 1 for i in best_player]
        new_array = []
        for i in range(len(array)):
            if i in indices:
                new_array.append([max(array[i])])
        best_index = GameLogic.find_highest_card_array(new_array)
        best_index = [i - 1 for i in best_index]
        best_player_new = []
        for i in range(len(best_index)):
            best_player_new.append(best_player[best_index[i]])
        return best_player_new

    '''-------------------------------------------------------------------------------------'''
    ''' -------------------------------------THREE KIND-------------------------------------'''
    '''-------------------------------------------------------------------------------------'''
    
    def three_kind(hand_numbers):
        
        array = hand_numbers
        # convert 1's to 14's for A's
        array = GameLogic.fourteens_for_aces(array)
        # find trips
        indices = []
        trip_list = []
        for i in range(len(array)):
            counter = Counter(array[i])
            trips = []
            if counter.most_common()[0][1] >= 3:
                trips.append(counter.most_common()[0][0])
                if counter.most_common()[1][1] >= 3:
                    trips.append(counter.most_common()[1][0])
                else:
                    pass
            if len(trips) >= 1:
                indices.append(i)
                trip_list.append(trips)
            else:
                pass
        # check if trips exists, if all nan, end here
        if GameLogic.nan_checker(trip_list, is2d=True) == True:
            return [None]
        # find best trips per person, if and only if, more than 1 trips in hand.
        for i in range(len(trip_list)):
            if len(trip_list[i]) > 1:
                trip_list[i] = [max(trip_list[i])]
            else:
                pass
        # find best trips in group
        trip_list_new = []
        indices_new = []
        for i in range(len(trip_list)):
            if trip_list[i] == np.nanmax(trip_list):
                trip_list_new.append(trip_list[i])
                indices_new.append(indices[i])
            else:
                pass
        # if 1 return done, else continue on
        if len(indices_new) == 1:
            best_player = [i+1 for i in indices_new]
            return best_player
        else:    
            # remove trips from each list
            new_array = []
            for i in range(len(trip_list_new)):
                temp = array[indices_new[i]]
                temp_new = sorted([x for x in temp if x != trip_list_new[0]])
                new_array.append(temp_new[-2:])
            
            # find highest remaining cards
            best_player = GameLogic.find_highest_card_array(new_array)
            return best_player
        
    '''-------------------------------------------------------------------------------------'''
    ''' -------------------------------------STRAIGHT---------------------------------------'''
    '''-------------------------------------------------------------------------------------'''

    def straight(hand_numbers):
        
        straight_hands = hand_numbers
        # make A's 14, and 1's, then sort each hand. Some will be longer than others because A is 2 values.
        straight_hands_temp = []
        for i in range(len(straight_hands)):
            temp_straight_hands = []
            for j in range(len(straight_hands[i])):
                if straight_hands[i][j] == 1:
                    temp_straight_hands.append(straight_hands[i][j])
                    temp_straight_hands.append(14)
                else:
                    temp_straight_hands.append(straight_hands[i][j])
            straight_hands_temp.append(sorted(temp_straight_hands))
        # get rid of pairs, trips, quads, and sort. Insert nan's for less than 5 cards left.
        new_hand = []
        for i in range(len(straight_hands_temp)):
            dummy = Counter(straight_hands_temp[i])
            if len(dummy.most_common()) >= 5:
                temp = []
                for j in range(len(dummy.most_common())):
                    temp.append(dummy.most_common()[j][0])
                new_hand.append(sorted(temp, reverse=True))
            else:
                new_hand.append([np.nan])
        # check for all nan's and kill here is True
        if GameLogic.nan_checker(new_hand) == True:
            return [None]
        # create a list that captures index of non nan lists in 2d list, also captures new 2d list
        index_list = []
        no_nan_list = []
        for i in range(len(new_hand)):
            if new_hand[i] == [np.nan]:
                pass
            else:
                index_list.append(i)
                no_nan_list.append(new_hand[i])
        # find hands with straights
        new_index_list = []
        new_no_nan_list = []
        for i in range(len(no_nan_list)):
            temp = no_nan_list[i]
            counter = 1
            for j in range(len(temp)):
                if temp[j] + 1 in temp:
                    counter += 1
                else:
                    if counter < 5:
                        counter = 1
                    else:
                        break
            if counter >= 5:
                new_index_list.append(index_list[i])
                new_no_nan_list.append(temp)
            else:
                pass
        if len(new_index_list) == 0:
            return [None]
        elif len(new_index_list) == 1:
            best_player = new_index_list[0] + 1
            return [best_player]
        else:
            # Ensure all lists in 2d array are of same size(5)
            for i in range(len(new_no_nan_list)):
                if len(new_no_nan_list[i]) != 5:
                    new_no_nan_list[i] = new_no_nan_list[i][:5]
                else:
                    pass
            # find best straights
            best_player = GameLogic.find_highest_card_array(new_no_nan_list)
            index = [i-1 for i in best_player]
            best_player = [new_index_list[i] for i in index]
            return best_player

    '''-------------------------------------------------------------------------------------'''
    ''' -------------------------------------FLUSH------------------------------------------'''
    '''-------------------------------------------------------------------------------------'''
            
    def flush(hand_numbers, hand_suits):
        full_hands = list(zip(hand_numbers, hand_suits))
        
        # i is each hand numbers and suits (#players)
        # j is each hand numbers or suits (2)
        # k is each hand 1 number or 1 suit (7)
        
        # this part grabs i, j, k stuff
        indices = []
        kindices = []
        most_common_list = []
        for i in range(len(full_hands)):
            counter = Counter(full_hands[i][1])
            if counter.most_common()[0][1] >= 5:
                kindex = []
                for k in range(len(full_hands[i][1])):
                    if full_hands[i][1][k] == counter.most_common()[0][0]:
                        kindex.append(k)
                most_common_list.append(counter.most_common()[0][0])
                indices.append(i)
                kindices.append(kindex)
                        
        # nan checker. kill function here is empty or all nan indicating no flush
        if GameLogic.nan_checker(most_common_list, is2d=False) == True:
            return [None]
        
        # get the hand numbers for all the flush hands with only the numbers associated with that suit.
        flush_hands = [full_hands[i] for i in indices]
        best_flush_hands = []
        for i in range(len(flush_hands)):
            best_flush_hands.append([flush_hands[i][0][j] for j in kindices[i]])
            
        # change 1's to 14's for A's
        best_flush_hands = GameLogic.fourteens_for_aces(best_flush_hands)
        
        # reduce down to best 5 cards by sorting and clipping.
        sorted_hands = GameLogic.sort_2d_array(best_flush_hands)
        for i in range(len(sorted_hands)):
            sorted_hands[i] = sorted_hands[i][-5:]

        # end func here is length is only 1.
        if len(sorted_hands) == 1:
            best_player = [i + 1 for i in indices]
            return best_player

        # find best flush now
        else:
            best_array = GameLogic.find_highest_card_array(sorted_hands)
            best_array = [i - 1 for i in best_array]
            best_player = []
            for i in range(len(best_array)):
                best_player.append(indices[best_array[i]])
            best_player = [i + 1 for i in best_player]
            return best_player

    '''-------------------------------------------------------------------------------------'''
    ''' -------------------------------------FULL HOUSE-------------------------------------'''
    '''-------------------------------------------------------------------------------------'''

    def full_house(hand_numbers):
        
        array = hand_numbers
        # convert 1's to 14's for A's
        array = GameLogic.fourteens_for_aces(array)
        # find all trips
        trip_list = []
        for i in range(len(array)):
            counter = Counter(array[i])
            trips = []
            if counter.most_common()[0][1] >= 3:
                trips.append(counter.most_common()[0][0])
                if counter.most_common()[1][1] >= 3:
                    trips.append(counter.most_common()[1][0])
                else:
                    pass
            
            if len(trips) >= 1:
                trip_list.append(trips)
            else:
                trip_list.append([np.nan])
        
        # check if trips exists, if all nan, end here
        if GameLogic.nan_checker(trip_list, is2d=True) == True:
            return [None]
        
        # find best trips per person, if and only if, more than 1 trips in hand.
        for i in range(len(trip_list)):
            if len(trip_list[i]) > 1:
                trip_list[i] = [np.nanmax(trip_list[i])]
            else:
                pass
        # remove trips from array
        new_array = []
        for j in range(len(array)):
            if trip_list[j] != [np.nan]:
                new_array.append([i for i in array[j] if i != trip_list[j][0]])
            else:
                new_array.append([np.nan])
        
        # find all pairs in new_array to go with the trips.
        all_pairs = []
        for i in range(len(new_array)):
            counter = Counter(new_array[i])
            if counter.most_common()[0][1] >= 2:
                pairs = []
                for j in range(len(counter.most_common())):
                    if counter.most_common()[j][1] >= 2:
                        pairs.append(counter.most_common()[j][0])
                    else:
                        pass
                    
                if len(pairs) > 1:
                    pairs = sorted(pairs)
                    pairs = pairs[-1:]
                    for j in range(len(pairs)):
                        new_array[i].remove(pairs[j])
                        new_array[i].remove(pairs[j])
                else:
                    for j in range(len(pairs)):
                        new_array[i].remove(pairs[j])
                        new_array[i].remove(pairs[j])
                all_pairs.append(pairs)
            else:
                all_pairs.append([np.nan])
        # append pairs to trip_list 
        for i in range(len(trip_list)):
            if trip_list[i] != [np.nan] and all_pairs[i] != [np.nan]:
                trip_list[i].append(all_pairs[i][0])
            else:
                trip_list[i] = [np.nan]
        # end function below if all nan values, meaning no players have a full house.
        if GameLogic.nan_checker(trip_list) == True:
            return [None]
        
        #find best trips first
        pairs = [i[1] if i != [np.nan] else np.nan for i in trip_list]
        trips = [i[0] if i != [np.nan] else np.nan for i in trip_list]
        best_trips = []
        for i in range(len(trips)):
            if trips[i] == np.nanmax(trips):
                best_trips.append([trips[i]])
            else:
                best_trips.append([np.nan])
        best_player = [i + 1 for i, x in enumerate(best_trips) if x != [np.nan]]
        if len(best_player) == 1:
            return best_player
        # find best pair including only the indexes with best trips
        best_hand = []
        pairs = [np.nan if best_trips[i] == [np.nan] else pairs[i] for i, x in enumerate(pairs)]
        for i in range(len(pairs)):
            if best_trips[i] == [np.nan]:
                pairs[i] = np.nan
            if best_trips[i] != [np.nan] and pairs[i] == np.nanmax(pairs):
                best_hand.append([pairs[i]])
            else:
                best_hand.append([np.nan])
        best_player = []
        for i in range(len(best_hand)):
            if best_hand[i] != [np.nan]:
                best_player.append(i+1)
        return best_player

    '''-------------------------------------------------------------------------------------'''
    ''' -------------------------------------QUADS------------------------------------------'''
    '''-------------------------------------------------------------------------------------'''

    def four_kind(hand_numbers):
        array = hand_numbers
        # convert 1's to 14's for A's
        array = GameLogic.fourteens_for_aces(array)
        
        # find all quads
        quad_list = []
        for i in range(len(array)):
            counter = Counter(array[i])
            if counter.most_common()[0][1] == 4:
                quad_list.append([counter.most_common()[0][0]])
            else:
                quad_list.append([np.nan])
        # check if quads exists, if all nan, end here
        if GameLogic.nan_checker(quad_list, is2d=True) == True:
            return [None]
        
        # find best quads
        quads = [i[0] if i != [np.nan] else np.nan for i in quad_list]
        best_quads = []
        for i in range(len(quads)):
            if quads[i] == np.nanmax(quads):
                best_quads.append([quads[i]])
            else:
                best_quads.append([np.nan])
        best_player = [i + 1 for i, x in enumerate(best_quads) if x != [np.nan]]
        if len(best_player) == 1:
            return best_player
        
        # if multiple, find best highcard
        indices = [i - 1 for i in best_player]
        new_array = [array[i] for i, x in enumerate(best_quads) if i in indices]
        new_best_quads = [best_quads[i] for i, x in enumerate(best_quads) if i in indices]
        high_card = []
        for i in range(len(new_array)):
            remainder = []
            for j in range(len(new_array[i])):
                if new_array[i][j] == new_best_quads[i][0]:
                    pass
                else:
                    remainder.append(new_array[i][j])
            high_card.append(np.nanmax(remainder))
        best_player = []
        for i in range(len(high_card)):
            if high_card[i] == np.nanmax(high_card):
                best_player.append(indices[i] + 1)
            else:
                pass
        return best_player

    '''-------------------------------------------------------------------------------------'''
    ''' -------------------------------------STRAIGHT FLUSH---------------------------------'''
    '''-------------------------------------------------------------------------------------'''        
        
    def straight_flush(hand_numbers, hand_suits):
        
        ######################
        # find the flush first
        ######################
        full_hands = list(zip(hand_numbers, hand_suits))
        
        # i is each hand numbers and suits (#players)
        # j is each hand numbers or suits (2)
        # k is each hand 1 number or 1 suit (7)
        
        # this part grabs i, j, k stuff
        indices = []
        kindices = []
        most_common_list = []
        for i in range(len(full_hands)):
            counter = Counter(full_hands[i][1])
            if counter.most_common()[0][1] >= 5:
                kindex = []
                for k in range(len(full_hands[i][1])):
                    if full_hands[i][1][k] == counter.most_common()[0][0]:
                        kindex.append(k)
                most_common_list.append(counter.most_common()[0][0])
                indices.append(i)
                kindices.append(kindex)
                        
        # nan checker. kill function here if empty or all nan indicating no flush
        if GameLogic.nan_checker(most_common_list, is2d=False) == True:
            return [None]
        
        # get the hand numbers for all the flush hands with only the numbers associated with that suit.
        flush_hands = [full_hands[i] for i in indices]
        best_flush_hands = []
        for i in range(len(flush_hands)):
            best_flush_hands.append([flush_hands[i][0][j] for j in kindices[i]])
            
        # best_flush_hands has every number of the flush cards for each player
            
        ##########################################
        # find best straight from best_flush_hands
        ##########################################
        
        straight_hands = best_flush_hands
        # make A's 14, and 1's, then sort each hand. Some will be longer than others because A is 2 values.
        straight_hands_temp = []
        for i in range(len(straight_hands)):
            temp_straight_hands = []
            for j in range(len(straight_hands[i])):
                if straight_hands[i][j] == 1:
                    temp_straight_hands.append(straight_hands[i][j])
                    temp_straight_hands.append(14)
                else:
                    temp_straight_hands.append(straight_hands[i][j])
            straight_hands_temp.append(sorted(temp_straight_hands))
        
        # find hands with straights (not trivial)
        new_indices = []
        best_hands = []
        for i in range(len(straight_hands_temp)):
            one_darray = straight_hands_temp[i]
            straight = [one_darray[0]]
            for j in range(len(one_darray)):
                try:
                    if one_darray[j] + 1 == one_darray[j+1]:
                        straight.append(one_darray[j] + 1)
                    else:
                        if len(straight) >= 5:
                            break
                        else:
                            straight = [one_darray[j+1]]
                except:
                    if one_darray[j] - 1 == one_darray[j-1]:
                        pass
                    else:
                        straight = [one_darray[j]]
            if len(straight) >= 5:
                new_indices.append(indices[i])
                best_hands.append(straight)
            else:
                pass
            
        # if none then None
        if len(best_hands) == 0:
            return [None]
            
        # if 1 return best player
        if len(best_hands) == 1:
            return [new_indices[0] + 1]
            
        # if more than 1, find the best straight flush now
        straight_flushes = [sorted(best_hands[i])[-5:] for i, x in enumerate(best_hands)]
        max_list = [max(straight_flushes[i]) for i, x in enumerate(straight_flushes)]
        index = [i for i, x in enumerate(max_list) if x == max(max_list)]
        best_player = [new_indices[i] for i in index]
        return best_player

class NoLimit_Holdem:
    
    def __init__(self, number_players):
        self.number_players = number_players
        
    def shuffle_deck(full_deck):
        shuffled_deck = full_deck.copy()
        random.shuffle(shuffled_deck)
        return shuffled_deck
    
    def deal_cards(number_players, shuffled_deck):
        first_card = []
        second_card = []
        for i in range(number_players):
            first_card.append(shuffled_deck[i])
        shuffled_deck = shuffled_deck[number_players:]
        
        for i in range(number_players):
            second_card.append(shuffled_deck[i])
        shuffled_deck = shuffled_deck[number_players:]
        
        whole_cards = list(zip(first_card, second_card))
        return whole_cards, shuffled_deck
        
    def flop(shuffled_deck):
        flop = shuffled_deck[0:3]
        shuffled_deck = shuffled_deck[3:]
        return flop, shuffled_deck
    
    def turn(shuffled_deck):
        turn = shuffled_deck[0]
        shuffled_deck = shuffled_deck[1:]
        return turn, shuffled_deck
    
    def river(shuffled_deck):
        river = shuffled_deck[0]
        shuffled_deck = shuffled_deck[1:]
        return river, shuffled_deck

class BestHand:

    def full_game_dealt(number_players, full_deck):
        deck = NoLimit_Holdem.shuffle_deck(full_deck)
        whole_cards, remaining_deck = NoLimit_Holdem.deal_cards(number_players, deck)
        flop, remaining_deck = NoLimit_Holdem.flop(remaining_deck)
        turn, remaining_deck = NoLimit_Holdem.turn(remaining_deck)
        river, remaining_deck = NoLimit_Holdem.river(remaining_deck)
        community_cards = flop + [turn] + [river]
        return whole_cards, flop, turn, river, community_cards
    
    def winning_hand(best_player, whole_cards, com_cards):
    
        if len(best_player) > 1:
            winning_list = []
            for i in range(len(best_player)):
                winning_hand = [whole_cards[best_player[i]-1]] + com_cards
                winning_list.append(winning_hand)
#            print('It is a draw between ', best_player)
#            print(winning_list)
            return best_player
        
        else:
            if best_player[0] == None:
#                print('no pairs, check high card next!!')
                return None
            else:
                winning_hand = [whole_cards[best_player[0]-1]] + com_cards
#                print('The winning hand is player ', best_player, ' with :', winning_hand)
                return best_player
            
    def find_best_hand(whole_cards, flop, turn, river, com_cards, count=True, best_player_bool=False):
        # 40 second runtime for 100 000 iterations
        hand_numbers = Hands.hand_numbers(Hands.all_hands(whole_cards, flop, turn, river), 
                                          whole_cards, flop, turn, river)
        hand_suits = Hands.hand_suits(Hands.all_hands(whole_cards, flop, turn, river), 
                                          whole_cards, flop, turn, river)
        best_player = Hands.straight_flush(hand_numbers, hand_suits)

        if best_player[0] != None:
            best_player = BestHand.winning_hand(best_player, whole_cards, com_cards)
            if count == True:
                return 'straight_flush'
            if best_player_bool == True:
                return best_player, 'straight_flush'
            else:
                print('Straight_flush!')
        else:
            best_player = Hands.four_kind(hand_numbers)
            if best_player[0] != None:
                best_player = BestHand.winning_hand(best_player, whole_cards, com_cards)
                if count == True:
                    return 'quads'
                if best_player_bool == True:
                    return best_player, 'quads'
                else:
                    print('quads!')
            else:
                best_player = Hands.full_house(hand_numbers)
                if best_player[0] != None:
                    best_player = BestHand.winning_hand(best_player, whole_cards, com_cards)
                    if count == True:
                        return 'full_house'
                    if best_player_bool == True:
                        return best_player, 'full_house'
                    else:
                        print('full_house!')
                else:
                    best_player = Hands.flush(hand_numbers, hand_suits)
                    if best_player[0] != None:
                        best_player = BestHand.winning_hand(best_player, whole_cards, com_cards)
                        if count == True:
                            return 'flush'
                        if best_player_bool == True:
                            return best_player, 'flush'
                        else:
                            print('flush!')
                    else:
                        best_player = Hands.straight(hand_numbers)
                        if best_player[0] != None:
                            best_player = BestHand.winning_hand(best_player, whole_cards, com_cards)
                            if count == True:
                                return 'straight'
                            if best_player_bool == True:
                                return best_player, 'straight'
                            else:
                                print('straight!')
                        else:
                            best_player = Hands.three_kind(hand_numbers)
                            if best_player[0] != None:
                                best_player = BestHand.winning_hand(best_player, whole_cards, com_cards)
                                if count == True:
                                    return 'trips'
                                if best_player_bool == True:
                                    return best_player, 'trips'
                                else:
                                    print('trips!')
                            else:
                                best_player = Hands.two_pair(hand_numbers)
                                if best_player[0] != None:
                                    best_player = BestHand.winning_hand(best_player, whole_cards, com_cards)
                                    if count == True:
                                        return 'two_pair'
                                    if best_player_bool == True:
                                        return best_player, 'two_pair'
                                    else:
                                        print('two_pair')
                                else:
                                    best_player = Hands.one_pair(hand_numbers)
                                    if best_player[0] != None:
                                        best_player = BestHand.winning_hand(best_player, whole_cards, com_cards)
                                        if count == True:
                                            return 'one_pair'
                                        if best_player_bool == True:
                                            return best_player, 'one_pair'
                                        else:
                                            print('one_pair')
                                    else:
                                        best_player = Hands.high_cards(hand_numbers)
                                        best_player = BestHand.winning_hand(best_player, whole_cards, com_cards)
                                        if count == True:
                                            return 'high_card'
                                        if best_player_bool == True:
                                            return best_player, 'high_card'
                                        else:
                                            print('high_card')
        return count

    def find_high_cards():
        hand_numbers = Hands.hand_numbers(whole_cards, flop, turn, river)
        # 20.5 second runtime for 100 000 iterations
        best_player = Hands.high_cards(hand_numbers)
        if best_player[0] != None:
            print('Highest Cards')
            print(BestHand.winning_hand(best_player, whole_cards, com_cards))
            print('\n###', com_cards, '###\n')
            print('---', whole_cards, '---\n')
            print('--------------------------------------------------')
        else:
            return None    

    def find_one_pair():
        hand_numbers = Hands.hand_numbers(whole_cards, flop, turn, river)
        # 20.9 second runtime for 100 000 iterations
        best_player = Hands.one_pair(hand_numbers)
        if best_player[0] != None:
            print('One Pair')
            print(BestHand.winning_hand(best_player, whole_cards, com_cards))
            print('\n###', com_cards, '###\n')
            print('---', whole_cards, '---\n')
            print('--------------------------------------------------')
        else:
            return None    

    def find_two_pair():
        hand_numbers = Hands.hand_numbers(whole_cards, flop, turn, river)
        # 20.1 second runtime for 100 000 iterations
        best_player = Hands.two_pair(hand_numbers)
        if best_player[0] != None:
            print('Two Pairs')
            print(BestHand.winning_hand(best_player, whole_cards, com_cards))
            print('\n###', com_cards, '###\n')
            print('---', whole_cards, '---\n')
            print('--------------------------------------------------')
        else:
            return None    

    def find_three_kind():
        hand_numbers = Hands.hand_numbers(whole_cards, flop, turn, river)
        # 19 seconds runtime for 100 000 iterations
        best_player = Hands.three_kind(hand_numbers)
        if best_player[0] != None:
            print('Trips')
            print(BestHand.winning_hand(best_player, whole_cards, com_cards))
            print('\n###', com_cards, '###\n')
            print('---', whole_cards, '---\n')
            print('--------------------------------------------------')
        else:
            return None    
    
    def find_straight():
        hand_numbers = Hands.hand_numbers(whole_cards, flop, turn, river)
        # 21.1 second runtime for 100 000 iterations
        best_player = Hands.straight(hand_numbers)
        if best_player[0] != None:
            print('Straight')
            print(BestHand.winning_hand(best_player, whole_cards, com_cards))
            print('\n###', com_cards, '###\n')
            print('---', whole_cards, '---\n')
            print('--------------------------------------------------')
        else:
            print('None')
            return None

    def find_flush():
        hand_numbers = Hands.hand_numbers(whole_cards, flop, turn, river)
        hand_suits = Hands.hand_suits(whole_cards, flop, turn, river)
        # 32 second runtime for 100 000 iterations
        best_player = Hands.flush(hand_numbers, hand_suits)
        if best_player[0] != None:
            print('Flush')
            print(BestHand.winning_hand(best_player, whole_cards, com_cards))
            print('\n###', com_cards, '###\n')
            print('---', whole_cards, '---\n')
            print('--------------------------------------------------')
        else:
            return None

    def find_full_house():
        hand_numbers = Hands.hand_numbers(whole_cards, flop, turn, river)
        # 20.1 second runtime for 100 000 iterations
        best_player = Hands.full_house(hand_numbers)
        if best_player[0] != None:
            print('Full House!')
            print(BestHand.winning_hand(best_player, whole_cards, com_cards))
            print('\n###', com_cards, '###\n')
            print('---', whole_cards, '---\n')
            print('--------------------------------------------------')
        else:
            return None

    def find_four_kind():
        hand_numbers = Hands.hand_numbers(whole_cards, flop, turn, river)
        # 19.2 second runtime for 100 000 iterations
        best_player = Hands.four_kind(hand_numbers)
        if best_player[0] != None:
            print('Quads!')
            print(BestHand.winning_hand(best_player, whole_cards, com_cards))
            print('\n###', com_cards, '###\n')
            print('---', whole_cards, '---\n')
            print('--------------------------------------------------')
        else:
            return None

    def find_straight_flush():
        hand_numbers = Hands.hand_numbers(whole_cards, flop, turn, river)
        hand_suits = Hands.hand_suits(whole_cards, flop, turn, river)
        # 33 second runtime for 100 000 iterations
        best_player = Hands.straight_flush(hand_numbers, hand_suits)
        if best_player[0] != None:
            print('Straight_flush!')
            print(BestHand.winning_hand(best_player, whole_cards, com_cards))
            print('\n###', com_cards, '###\n')
            print('---', whole_cards, '---\n')
            print('--------------------------------------------------')
        else:
            return None




