import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace')
values = {'2':2, '3':3, '4':4,'5':5, '6':6, '7':7, '8':8, '9':9, '10':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True


class Card:
    
    def __init__(self, suit, rank):     #Constructor method Card()
        self.suit = suit
        self.rank = rank
    
    def __str__(self):
        return self.rank + " of " + self.suit
    
class Deck:
    
    def __init__(self):
        self.deck = []      #Start with an empty list
        for i in suits:
            for j in ranks:
                self.deck.append(Card(i,j))
    
    def __str__(self):
        deck_comp =''       #Initialize as empty string
        for c in self.deck:
            deck_comp += ', ' + c.__str__()      #Store string of each card into deck_comp variable
        return 'The deck has: ' + deck_comp
    
    def shuffle(self):
        random.shuffle(self.deck)       #Shuffles the list of deck cards
    
    def deal(self):
        return self.deck.pop()
        
    
class Hand:
    def __init__(self):
        self.hand_cards = []     #Start with empty list for "hand cards" just like the Deck class
        self.value = 0      #Total value = 0 initially
        self.aces = 0       #Need to keep traack of aces
    
    def add_card(self, card):
        #from Deck.deal() --> where card (has suit, has rank) is popped from top of the Deck
        self.hand_cards.append(card)
        self.value += values[card.rank]
        
        #track aces
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_aces(self):
        while self.value > 21 and self.aces >0:     #If hand card values total >21, and we have an ace card
            self.value -= 10                        #then treat the ace as a "1" instead of a "11", subtr 10
            self.aces -= 1

class Chips:
    def __init__(self, total = 100):
        self.total = total      #Initialize total starting money, default = 100
        self.bet = 0            #Initialize money betted as 0
    
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet
    

def take_bet(chip):
    while True:
        try:
            chip.bet = int(input("How many chips do you want to bet?\n"))
        except ValueError:
            print('Sorry, you must enter an integer!')
        else:
            if chip.bet > chip.total:
                print('Sorry, your bet cannot exceed {}'.format(chip.total))
            else:
                break
        
def hit(deck, hand):
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_aces()

def hit_or_stand(deck, hand):
    global playing      #Global variable access to control while loop below
    while True:
        x = input("Hit or Stand? Enter 'h' or 's'\n")
        if x[0].lower() == 'h':
            hit(deck,hand)
        elif x[0].lower() == 's':
            print("Player Stands, Dealer's turn now...")
            playing = False
        else:
            print("Sorry, I did not understand that. Please enter 'h' or 's' only!")
            continue
        break

#Show player and dealer's hands of cards
def show_some(player, dealer):
    print("\nDealers Hand:")
    print(dealer.hand_cards[0])
    print('Other cards hidden\n')
    print("Your (Player's) Hand:")
    for i in range(len(player.hand_cards)):
        print(player.hand_cards[i])
    
def show_all(player, dealer):
    print("\nDealers Hand:")
    for i in range(len(dealer.hand_cards)):
        print(dealer.hand_cards[i])
    
    print("\nYour (Player's) Hand:")
    for i in range(len(player.hand_cards)):
        print(player.hand_cards[i])

#Functionst o handle end of game scenario

def player_loses(player, dealer, chips):
    print("Player loses...")
    chips.lose_bet()
    
def player_wins(player, dealer, chips):
     print("Player wins!!!")
     chips.win_bet()
     
def dealer_loses(player, dealer, chips):
    print("Dealer loses, so Player wins!!!!")
    chips.win_bet()
    
def dealer_wins(player, dealer, chips):
    print("Dealer wins, so Player loses...")
    chips.lose_bet()
    
def push(player, dealer):     #Means a tie, both at 21, so neither win nor loses   
    print("Dealer and Player are tied, no one wins! Push")


#Now implementation of the game, should be a new Class in another file
while True:
    print("Welcome to BlackJack!")
    
    #Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    
    #Set up the Player's chips with default 100
    player_chips = Chips()
    take_bet(player_chips)
    
    show_some(player_hand, dealer_hand)
    
    while playing: 
        hit_or_stand(deck, player_hand)
        show_some(player_hand, dealer_hand)
        if player_hand.value >21:
            player_loses(player_hand, dealer_hand, player_chips)
            break
        
    #If player hand didn't lose yet, keep playing
    if player_hand.value <= 21:
        while dealer_hand.value < player_hand.value:
            hit(deck,dealer_hand)
            
        #Show all cards from both parties
        show_all(player_hand, dealer_hand)
        
        if dealer_hand.value > 21:
            dealer_loses(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)
    
    #Inform player's remaining chips
    
    print('\nPlayer total chips are at: {}'.format(player_chips.total))
    
    #Ask to play again?
    new_game = input("Would you like to play again? 'y/n'")
    if new_game[0].lower() =='y':
        playing = True
        continue
    else:
        print('Thank you for playing!')
        break
    
    
        
        
        