import random
from enum import Enum

class Suit(Enum):
    SPADES = '♠'
    HEARTS = '♥'
    DIAMONDS = '♦'
    CLUBS = '♣'

class Rank(Enum):
    ACE = ('A', 11)
    TWO = ('2', 2)
    THREE = ('3', 3)
    FOUR = ('4', 4)
    FIVE = ('5', 5)
    SIX = ('6', 6)
    SEVEN = ('7', 7)
    EIGHT = ('8', 8)
    NINE = ('9', 9)
    TEN = ('10', 10)
    JACK = ('J', 10)
    QUEEN = ('Q', 10)
    KING = ('K', 10)
    
    @property
    def display_char(self):
        return self.value[0]

    @property
    def blackjack_value(self):
        return self.value[1]

class Card:
    def __init__(self, rank: Rank, suit: Suit):
        self.rank = rank
        self.suit = suit
        self.value = rank.blackjack_value
        self.display_char = rank.display_char

    def display_lines(self):
        underscores = "__" if len(self.display_char) == 1 else "_"
        spaces = "  " if len(self.display_char) == 1 else " " 
        suit_symbol = self.suit.value
        return [
            " ___ ",
            f"|{self.display_char}{spaces}|",
            f"| {suit_symbol} |",
            f"|{underscores}{self.display_char}|",
        ]

    def __str__(self):
        return f"{self.display_char}{self.suit.value}"

class Deck:
    def __init__(self):
        self._cards = []
        self.reset()

    def reset(self):
        self._cards.clear()
        for suit in Suit:
            for rank in Rank:
                self._cards.append(Card(rank, suit))

    def shuffle(self):
        random.shuffle(self._cards)

    def draw(self) -> Card | None:
        if self._cards:
            return self._cards.pop()
        return None

class Hand:
    def __init__(self, bet=0):
        self.cards = []
        self.bet = bet

    def add_card(self, card: Card):
        self.cards.append(card)

    def flush(self):
        self.cards.clear()

    def calculate_value(self) -> int:
        value = 0
        num_aces = 0
        for card in self.cards:
            if card.rank is Rank.ACE:
                num_aces += 1
            value += card.value
        while value > 21 and num_aces > 0:
            value -= 10
            num_aces -= 1
        return value

    def __str__(self):
        if not self.cards:
            return "Hand is empty."
        num_lines = len(self.cards[0].display_lines()) 
        lines = [""] * num_lines 
        for card in self.cards:
            card_lines = card.display_lines()
            for i in range(num_lines):
                lines[i] += card_lines[i] + " "
        return '\n'.join(lines)