import random


class Card:

    def __init__(self, rank, suit, up=True):
        self.rank = rank
        self.suit = suit
        self.up = up

    def get_value(self):
        if self.rank in ["Jack", "Queen", "King"]:
            return 10
        elif self.rank == "Ace":
            return 1
        else:
            return int(self.rank)

    @property
    def is_up(self):
        return self.up

    @is_up.setter
    def is_up(self, value):
        """
        Set whether the card is face up or face down.

        Args:
            up (bool): True if card is face up, False if face down
        """
        self.up = value

    def __str__(self):
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self):
        self.cards = []
        self.initialise_deck()

    def initialise_deck(self):
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        for suit in suits:
            for rank in ranks:
                card = Card(rank, suit)
                self.cards.append(card)


class BasePlayer:

    def __init__(self, name, points=0):
        self.cards = []
        self.name = name
        self.points = points

    def calculate_hand_value(self):
        """Calculate the value of a player's hand, accounting for Aces."""
        total = 0
        aces = 0
        # Count values and track aces
        for card in self.cards:
            if card.rank == "Ace":
                aces += 1
                total += 1  # Initially count Ace as 1
            else:
                total += card.get_value()
        # # Convert aces to 11 if beneficial
        while aces > 0 and total + 10 <= 21:
            total += 10
            aces -= 1

        return total


class Dealer(BasePlayer):
    def __init__(self, name, deck):
        super().__init__(name)
        self.deck = deck

    def deal(self, opponents):
        """
        opponents: list of players to deal to
        """
        for i in range(2):
            # deal cards for the dealer
            card = self.get_card_from_deck()
            # first card for the dealer is face down
            if i == 0:
                card.is_up = False
            self.cards.append(card)
            for opponent in opponents:
                opponent.cards.append(self.get_card_from_deck())

    def get_card_from_deck(self):
        return self.deck.cards.pop()

    def shuffle_deck(self):
        random.shuffle(self.deck.cards)


class Player(BasePlayer):
    def __init__(self, name):
        super().__init__(name)
        self.bets = []

    def place_bet(self, amount):
        self.bets.append(int(amount))


def help_text():
    return """
    Welcome to black jack game
    To deal a card its d
    To hold its h
    To double down its dd
    To split its s
    To quit its q
    To see the help text its h

    """

if __name__ == "__main__":
    deck = Deck()
    dealer = Dealer("Mr obuja", deck)
    players = []
    count = input("Enter the number of players: ")
    for i in range(int(count)):
        player = Player(input("Enter the name of player {}: ".format(i+1)))
        players.append(player)
    dealer.deal(players)
    for card in dealer.cards:
        print(card)
    while True:
        action = input(">>> ")
        if action == "q":
            break
        elif action == "h":
            print(help_text())
        elif not deck.cards:
            print("Deck is empty")
            break