from constant import *


class Game:
    def __init__(self, n):
        self.players = []
        self.dealer = Player(names.pop())
        self.dealer.cash = 0
        for i in range(n):
            self.players.append(Player(names.pop()))

    def addPlayer(self, name):
        self.players.append(Player(name))

    def clearPlayerHands(self):
        for p in self.players:
            p.hand = []
        self.dealer.hand = []

    def giveRewards(self):
        d = self.dealer
        v = d.getHandValue()
        if (max(v) <= 21):
            dv = max(v)
        else:
            dv = min(v)
        for p in self.players:
            v = p.getHandValue()
            if (max(v) <= 21):
                pv = max(v)
            else:
                pv = min(v)
            if (pv <= 21 and (pv > dv or dv > 21)):
                if (pv == dv):
                    p.cash += p.bet
                else:
                    p.cash += 2 * p.bet
                    d.cash -= p.bet
            else:
                d.cash += p.bet
            p.bet = 0

    def printStatus(self):
        print("------------------------------")
        print("Cards remaining: " + str(deck.length()))
        print("Count: " + str(deck.count))
        print("\r")
        print("Dealer '" + self.dealer.name + "' cash: " + str(
            self.dealer.cash) + " - hand: " + self.dealer.handToStr() + " (" + ",".join(
            str(x) for x in self.dealer.getHandValue()) + ")")
        for p in self.players:
            print(p.name + " cash: " + str(p.cash) + " - hand:" + p.handToStr() + " (" + ",".join(
                str(x) for x in p.getHandValue()) + ")")
        print("------------------------------")
        print("\n")


class Player:
    def __init__(self, name):
        self.name = name
        self.hand = []
        self.cash = 1000
        self.bet = 0

    def giveCard(self):
        c = deck.cards.pop()
        if c.value == "R":
            deck.renew = True
            c = deck.cards.pop()
        self.hand.append(c)
        deck.updateCount(c)

    def getHandValue(self):
        v = [0]
        for c in self.hand:
            if c.value == "A":
                for i in range(len(v)):
                    v.append(v[i] + 11)
                    v[i] += 1
            elif (type(c.value) is str or c.value == 10):
                v = [x + 10 for x in v]
            else:
                v = [x + c.value for x in v]
        return v

    def isHard(self):
        v = self.getHandValue()
        ace = False
        for card in self.hand:
            if card.value == "A": #There is an Ace
                ace = True
        if not ace: #If there is no Aces, it's a hard hand
            return True
        if(min(v)>10):
            return True #If an Ace can still be 1 and 11, it's a hard hand
        else:
            return False #If not, it's a soft hand

    # BEST HEURISTIC EUW:
    def nextAction(self):
        v = self.getHandValue()
        d = game.dealer
        if (min(v) > 21):
            return BUST
        elif (17 in v or 18 in v or 19 in v or 20 in v or 21 in v):
            return STAND
        else:
            return HIT

    def handToStr(self):
        s = ""
        for c in self.hand:
            s += str(c.value) + str(c.suit) + ","
        return s[:-1]


class Deck:
    def __init__(self, n):
        self.cards = []
        self.count = 0
        self.renew = False
        for i in range(n):
            for s in suits:
                for v in values:
                    self.cards.append(Card(v, s))
        random.shuffle(self.cards)
        self.cards.insert(int(len(self.cards) / 2), Card("R", "R"))

    def printDeck(self):
        for c in self.cards:
            print(c)

    def length(self):
        return len(self.cards)

    def updateCount(self, card):
        if (type(card.value) is str or card.value == 10):
            self.count -= 1
        elif (card.value < 7):
            self.count += 1


class Card:
    def __init__(self, value, suit):
        self.value = value
        self.suit = suit

    def __str__(self):
        return str(self.value) + str(self.suit)


deck = Deck(NUM_DECKS)
game = Game(NUM_PLAYERS)


def playRound(debug=False):
    game.clearPlayerHands()
    if (deck.renew == True):
        deck.__init__(NUM_DECKS)
        print("Cards renewed and shuffled!")
    for p in game.players:  # Place your bets!!
        if (p.cash >= 100):
            p.bet += 100
            p.cash -= 100
        else:
            print("Player " + p.name + " out of money, GTFO!")
            game.players.remove(p)

    for p in game.players:
        p.giveCard()  # One card for each player
    game.dealer.giveCard()  # One card for the dealer

    for p in game.players:
        p.giveCard()  # And again one card for each player
    if (debug):
        game.printStatus()
        # input()

    for p in game.players:
        act = p.nextAction()
        if (debug):
            hand_type = ("HARD","SOFT")[p.isHard()]
            print("Player " + p.name + " has this hand:[" + p.handToStr() + "] (" + ",".join(str(x) for x in p.getHandValue()) + ")(" + hand_type + "), action:" + actions[act])
        while (not (act == STAND or act == BUST)):
            if (act == HIT):
                p.giveCard()
            act = p.nextAction()
            if (debug):
                hand_type = ("HARD","SOFT")[p.isHard()]
                print("Player " + p.name + " has this hand:[" + p.handToStr() + "] (" + ",".join(str(x) for x in p.getHandValue()) + ")(" + hand_type + "), action:" + actions[act])

    act = game.dealer.nextAction()
    while (not (act == STAND or act == BUST)):
        if (act == HIT):
            game.dealer.giveCard()
        act = game.dealer.nextAction()

    game.giveRewards()


def playSingleGame(debug=False):
    playRound(debug)
    # game.printStatus()


def playManyGames(n):
    for i in range(n):
        playRound()
    game.printStatus()


def restartGame():
    global deck, game
    deck = Deck(NUM_DECKS)
    game = Game(NUM_PLAYERS)

# playManyGames(100)
playSingleGame(DEBUG)
