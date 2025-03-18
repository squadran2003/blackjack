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

    def __init__(self, name, points=0, turn=False):
        self.cards = []
        self.name = name
        self.points = points
        self.turn = turn

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

    def hit(self, dealer):
        self.cards.append(dealer.get_card_from_deck())
        # Check for bust after hitting
        if self.has_busted:
            self.turn = False
            print(f"{self.name} busts with {self.calculate_hand_value()}!")

    @property
    def has_busted(self):
        return self.calculate_hand_value() > 21


class Dealer(BasePlayer):
    def __init__(self, name, deck):
        super().__init__(name,points=0, turn=False)
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
        super().__init__(name, points=0, turn=False)
        self.bet = 0

    def place_bet(self, amount):
        self.bet += amount

    def stand(self):
        self.turn = False

    def double_down(self):
        self.bet *= 2
        self.hit()
        self.stand()


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


def has_player_won(player, dealer):
    """
    player: Player
    dealer: Dealer

    return tuple: True, bets won, False, bets lost
    """
    if player.has_busted:
        return False, player.bet
    elif dealer.has_busted:
        return True, player.bet
    elif player.calculate_hand_value() > dealer.calculate_hand_value():
        return True, player.bet
    else:
        return False, player.bet

if __name__ == "__main__":
    deck = Deck()
    dealer = Dealer("Dealer", deck)
    dealer.shuffle_deck()

    # Setup players
    players = []
    count = input("Enter the number of players: ")
    for i in range(int(count)):
        player = Player(input(f"Enter the name of player {i+1}: "))
        players.append(player)

    playing = True
    while playing:
        # New round setup
        dealer.cards = []
        for player in players:
            player.cards = []
            bet = int(input(f"{player.name}, place your bet: "))
            player.place_bet(bet)
            player.turn = True

        # Deal cards
        dealer.deal(players)

        # Show initial hands
        print("\nDealer shows:", dealer.cards[1])

        # Player turns
        for player in players:
            print(f"\n{player.name}'s turn:")
            print(f"Cards: {', '.join(str(card) for card in player.cards)}")
            print(f"Total: {player.calculate_hand_value()}")

            while player.turn:
                action = input("Action (h-hit, s-stand, dd-double down, ?-help, q-quit): ")
                if action == "h":
                    player.hit(dealer)
                    print(f"Cards: {', '.join(str(card) for card in player.cards)}")
                    print(f"Total: {player.calculate_hand_value()}")
                elif action == "s":
                    player.stand()
                    print(f"{player.name} stands with {player.calculate_hand_value()}")
                elif action == "dd":
                    player.double_down(dealer)
                    print(f"Doubled down! New bet: {player.bet}")
                    print(f"Cards: {', '.join(str(card) for card in player.cards)}")
                    print(f"Total: {player.calculate_hand_value()}")
                elif action == "?":
                    print(help_text())
                elif action == "q":
                    playing = False
                    player.turn = False
        if playing:
            # Dealer's turn
            dealer.play_turn()

            # Determine winners and update scores
            for player in players:
                won, amount = has_player_won(player, dealer)
                if won:
                    print(f"{player.name} wins ${amount}!")
                    player.points += amount
                else:
                    print(f"{player.name} loses ${amount}")
                    player.points -= amount
                print(f"{player.name}'s total points: {player.points}")

            # Ask to play another round
            again = input("\nPlay another round? (y/n): ").lower()
            if again != 'y':
                playing = False