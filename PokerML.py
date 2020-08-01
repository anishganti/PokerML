import random
import itertools

# Hearts, Diamonds, Clubs, Spade
suits = ('Hearts', 'Diamonds', 'Clubs', 'Spades')

# Possible card ranks
ranks = ('Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', "Queen", 'King')

# Point values
points = {'Ace': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7,
          '8': 8, '9': 9, '10': 10, 'Jack': 11, 'Queen': 12, 'King': 13}


class Card:
    # Create card class
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def getSuit(self):
        return self.suit

    def getRank(self):
        return self.rank

    def getPoints(self):
        return points.get(self.rank)

    def toString(self):
        return self.rank + " of " + self.suit


class Deck:
    # Create deck class
    def __init__(self):
        self.deck = []
        # Create deck of 52 cards
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def shuffleDeck(self):
        # Shuffle randomly
        random.shuffle(self.deck)

    def getCard(self):
        # Gets card on top of deck
        card = self.deck[0]
        # Remove card from play
        self.deck.remove(card)
        return card


class Table:
    def __init__(self):
        # Create a 'board' for community cards
        self.communityCards = []
        # Create a pot of money
        self.pot = 0

    def addCard(self, card):
        # Add card to community board
        self.communityCards.append(card)

    def getCards(self):
        # Return all community cards
        return self.communityCards

    def showTable(self):
        # Print all cards on table
        for i in range(len(self.communityCards)):
            print(self.communityCards[i].toString)

    def addPot(self, money):
        # Add money to pot
        self.pot += money

    def setPot(self, price):
        # Set pot to price
        self.pot = price


class Player(object):
    # Player is computer object
    def __init__(self, name):
        # Create a 'hand' and a pool
        self.name = name
        self.hand = []
        self.money = 1000
        self.moves = ("fold", "raise", "call", "bet")

    def addHand(self, card):
        # Add card to hand
        self.hand.append(card)

    def getHand(self):
        # hand getter method
        return self.hand

    def betMoney(self, table, money):
        # Bet some of your money, add it to pot
        self.money -= money
        table.addPot(money)

    def makeMove(self):
        move = random.choice(self.moves)
        pass

    def getName(self):
        # Return player name
        return self.name


class User(Player):
    # physical person playing
    def __init__(self):
        # Create a 'hand' and a pool
        super().__init__(input("Your Name: "))

    def makeMove(self):
        move = input("What is your move:")
        pass


def communityFlop(deck, board):
    # Flop, put 3 cards on the table
    for i in range(3):
        board.addCard(deck.getCard())


def communityTurn(deck, board):
    # Turn, put 4th card on the table
    board.addCard(deck.getCard())


def communityRiver(deck, board):
    # River, put 5th and final card on table
    board.addCard(deck.getCard())


def dealHoleCards(deck, players):
    # Deal 2 'hole' cards at beginning of game
    for player in players:
        for i in range(2):
            player.addHand(deck.getCard())


def postBlinds(players, table):
    # Post small blind and big blind two player
    players[1].betMoney(table, money=int(input("Small Blind: ")))
    players[0].betMoney(table, money=int(input("Big Blind ")))
    # Reverse so that next round blinds are reversed
    players.reverse()


def getWinner(players, table):
    maxi = 0
    name = ""
    for player in players:
        score = getScores(player, table)
        maxi = score if score > maxi else maxi
        name = player.getName() if maxi == score else name
    print(name)
    print(score)


def getScores(player, table):
    maxScore = 0
    cards = player.getHand()[:] + table.getCards()[:]
    for comb in itertools.combinations(cards, 5):
        handScore = evaluateScore(list(comb))
        maxScore = handScore if handScore > maxScore else maxScore
    return maxScore


def evaluateScore(hands):
    cards = hands[:]
    # Check for a flush
    isFlush = True
    flush = cards[0].getSuit()
    for card in cards:
        if card.getSuit() is not flush:
            isFlush = False

    # Check for a straight
    isStraight = True
    # Sort cards by increasing rank
    cards.sort(key=lambda card_: card_.getPoints())
    for i in range(1, len(cards)):
        if cards[i].getPoints() - 1 != cards[i - 1].getPoints():
            isStraight = False

    # Check for royal flush
    if isStraight and isFlush:
        isRoyal = False
        # Do royal flush check
        if isRoyal:
            return 10
        else:
            return 9

    # Check for four of a kind, only two ways
    if cards[0].getPoints() == cards[3].getPoints() or cards[1].getPoints() == cards[4].getPoints():
        return 8

    # Check for full house
    if ((cards[0].getPoints() == cards[1].getPoints() and cards[2].getPoints() == cards[4].getPoints()) or
        (cards[0].getPoints() == cards[2].getPoints() and cards[3].getPoints() == cards[4].getPoints())):
        return 7

    if isFlush:
        return 6

    if isStraight:
        return 5

    # Check for three of a kind, only three ways
    if cards[0].getPoints() == cards[2].getPoints() or (cards[1].getPoints() == cards[3].getPoints()
       or cards[2].getPoints() == cards[4].getPoints()):
        return 4

    # Check for two pairs, only two ways
    if ((cards[0].getPoints() == cards[1].getPoints() and cards[2].getPoints() == cards[3].getPoints()) or
        (cards[1].getPoints() == cards[2].getPoints() and cards[3].getPoints() == cards[4].getPoints())):
        return 3

    # Check for a single pair
    for i in range(1, len(cards)):
        if cards[i].getPoints() == cards[i - 1].getPoints():
            return 2

    # No combination, return high card
    return 1


def main():
    # Main method and logic
    # Initialize all objects
    deck = Deck()
    deck.shuffleDeck()
    table = Table()
    players = [Player("Bot"), User()]
    # Deal hole cards
    dealHoleCards(deck, players)
    # Pre-flop Betting
    postBlinds(players, table)
    # Flop
    communityFlop(deck, table)
    for player in players:
        player.makeMove()
    # Turn
    communityTurn(deck, table)
    for player in players:
        player.makeMove()
    # River
    communityRiver(deck, table)
    for player in players:
        player.makeMove()
    getWinner(players, table)

main()
