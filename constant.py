import random

BUST = 0
HIT = 1
STAND = 2
SPLIT = 3
DOUBLE = 4

NUM_DECKS = 6 #6-8
NUM_PLAYERS = 5 #MAX 7

values = ["A",2,3,4,5,6,7,8,9,10,"J","Q","K"]
suits = ['C','D','H','S'] #Clubs, Diamonds, Hearts, Spades

names = ["Nick","John","Matthew","Bill","Carl","Nathan","Robert","Martha"]
random.shuffle(names)