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
        # Consider conditional display based on card visibility
        if not self.is_up:
            return "Card face down"
        return f"{self.rank} of {self.suit}"


class Deck:
    def __init__(self):
        self.cards = []
        self.initialise_deck()

    def initialise_deck(self):
        """Create a deck of 52 cards."""
        suits = ["Hearts", "Diamonds", "Clubs", "Spades"]
        ranks = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
        for suit in suits:
            for rank in ranks:
                card = Card(rank, suit)
                self.cards.append(card)

    def reset_deck(self):
        self.cards = []
        self.initialise_deck()


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
    
    def hit(self, dealer):
        """ get a new card from the dealer """
        self.cards.append(dealer.get_card_from_deck())

    def has_busted(self):
        return self.calculate_hand_value() > 21


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
        if not self.deck.cards:
            raise ValueError("Cannot draw from empty deck, Try reseting the deck")
        return self.deck.cards.pop()

    def shuffle_deck(self):
        random.shuffle(self.deck.cards)


class Player(BasePlayer):
    def __init__(self, name, has_won=False):
        super().__init__(name)
        self.bets = []
        self.has_won = has_won
        self.balance = 0

    def set_balance(self, amount):
        self.balance = amount

    def win_bet(self):
        winnings = self.bets[-1]
        self.balance += winnings
        return winnings

    def lose_bet(self):
        losses = self.bets[-1]
        self.balance -= losses
        return losses

    def place_bet(self, amount):
        self.bets.append(int(amount))

    def clear(self):
        self.cards = []
        self.bets = []


def help_text():
    return """
    Welcome to black jack game
    To deal a card its d
    To hit its h
    To double down its dd
    To stand its s
    To quit its q
    To see the help text its h

    """

if __name__ == "__main__":
    print(help_text())
    players = []
    count = input("Enter the number of players: ")
    for i in range(int(count)):
        player = Player(input("Enter the name of player {}: ".format(i+1)))
        players.append(player)
    playing = True
    while playing:
        deck = Deck()
        dealer = Dealer("Mr obuja", deck)
        dealer.shuffle_deck()
        # reset player cards
        [player.cards.clear() for player in players]
        dealer.deal(players)
        for player in players:
            print("----------------------------------------------------------------------")
            balance = input("Enter the balance for player {}: ".format(player.name))
            player.set_balance(int(balance))
            print("----------------------------------------------------------------------")
            bet = input("Enter the bet amount for player {}: ".format(player.name))
            player.place_bet(bet)
        # dealer reveals his hidden card
        print("----------------------------------------------------------------------")
        dealer.cards[0].is_up = True
        print("Dealer facedown card is: ", dealer.cards[0])
        print("Dealer faceup card is: ", dealer.cards[1])
        print(f"Dealer hand value is {dealer.calculate_hand_value()}")

        for player in players:
            print("----------------------------------------------------------------------")
            print(f"{player.name} has the following cards")
            for card in player.cards:
                print(f"{player.name}: {card}")
            print(f"{player.name} has a hand value of {player.calculate_hand_value()}")
            print("Player: ", player.name)
            action = input("""
            d to deal
            s to stand ( keep current hand)
            h to hit ( take another card )
            dd to double down ( take exactly one more card )
            q to quit
            Enter the action: """)
            if player.has_busted():
                print(f"{player.name} has busted")
                player.has_won = False
                player.lose_bet()
                continue
            if action == "q":
                break
            elif action == "h":
                player.hit(dealer)
                option = input("Do you want to hit again? y/n: ")
                while option == "y":
                    print("----------------------------------------------------------------------")
                    player.hit(dealer)
                    option = input("Do you want to hit again? y/n: ")
            elif action == "s":
                continue
            elif action == "dd":
                player.hit(dealer)
                player.place_bet(player.bets[-1])
            elif not deck.cards:
                print("Deck is empty")
                break

        dealer_dealing = True
        while dealer_dealing:
            if dealer.calculate_hand_value() < 17:
                dealer.hit(dealer)
            else:
                dealer_dealing = False
        player_value = player.calculate_hand_value()
        dealer_value = dealer.calculate_hand_value()

        if dealer.has_busted():
            print(f"{player.name} wins! Dealer busted.")
            # all players win
            for player in players:
                player.has_won = True
                player.win_bet()
            # Handle winnings
        elif player_value > dealer_value:
            print(f"{player.name} wins with {player_value} vs dealer's {dealer_value}")
            player.has_won = True
            player.win_bet()
            # Handle winnings
        elif player_value < dealer_value:
            print(f"{player.name} loses with {player_value} vs dealer's {dealer_value}")
            player.has_won = False
            player.lose_bet()
        else:
            print(f"{player.name} pushes with dealer at {player_value}")
        # check if player gets a natural blackjack
        if player_value == 21 and not dealer_value == 21:
            print(f"{player.name} has a natural blackjack and has won")
            player.has_won = True
        for player in players:
            if player.has_won:
                print(f"{player.name} has won the game")
                print(f"{player.name} has a balance of {player.balance}")
            else:
                print(f"{player.name} has lost the game")
                print(f"{player.name} has a balance of {player.balance}")
        playing = False
        option = input("Do you want to play again? y/n: ")
        if option == "y":
            playing = True
        else:
            break

            