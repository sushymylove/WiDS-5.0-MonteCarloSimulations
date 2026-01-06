import random
from cards import Deck, Hand, Card, Rank 

def calculate_winnings(outcome: str, bet: int) -> int:
    if "BLACKJACK (pays 1.5x)" in outcome:
        return int(bet * 1.5)
    if "PLAYER WINS" in outcome:
        return bet
    if "PUSH" in outcome:
        return 0
    return -bet

class BlackJack:
    def __init__(self):
        self.deck = Deck()
        self.player_hands = []
        self.dealer_hand = Hand()
        self.active_hand_index = 0
        self.is_doubling_down = False

    def start_match(self, initial_bet):
        self.deck.reset()
        self.deck.shuffle()
        self.dealer_hand.flush()
        self.player_hands = [Hand(initial_bet)]
        self.active_hand_index = 0
        self.is_doubling_down = False
        self._deal_initial_cards()
        return self._check_initial_win_conditions()

    def _deal_initial_cards(self):
        for _ in range(2):
            self.player_hands[0].add_card(self.deck.draw())
            self.dealer_hand.add_card(self.deck.draw())

    def _check_initial_win_conditions(self) -> str | None:
        p_hand = self.player_hands[0]
        player_21 = p_hand.calculate_value() == 21 and len(p_hand.cards) == 2
        dealer_21 = self.dealer_hand.calculate_value() == 21 and len(self.dealer_hand.cards) == 2
        
        if player_21 or dealer_21:
            if player_21 and dealer_21:
                return "PUSH: Both have Blackjack."
            if player_21:
                return "PLAYER WINS: BLACKJACK (pays 1.5x)." 
            if dealer_21:
                return "DEALER WINS: Dealer BLACKJACK."
        return None

    def get_active_hand(self):
        return self.player_hands[self.active_hand_index]

    def hit(self) -> tuple[str, bool]:
        hand = self.get_active_hand()
        hand.add_card(self.deck.draw())
        card_name = str(hand.cards[-1])
        
        if self._is_busted(hand):
            return (f"You drew a {card_name}. Player busted!", True)
        
        if self.is_doubling_down:
            return (f"You drew a {card_name}. Mandatory stand after double down.", True)
        
        return (f"You drew a {card_name}.", False)

    def stand(self) -> tuple[str, bool]:
        return ("Player stands.", True)

    def double_down(self) -> tuple[str, bool]:
        self.is_doubling_down = True
        return self.hit()

    def split(self):
        current = self.get_active_hand()
        new_hand = Hand(current.bet)
        new_hand.add_card(current.cards.pop())
        current.add_card(self.deck.draw())
        new_hand.add_card(self.deck.draw())
        self.player_hands.insert(self.active_hand_index + 1, new_hand)

    def dealer_play(self) -> str:
        print("\n--- Dealer's Turn ---")
        if len(self.dealer_hand.cards) == 2:
            print("\n** Dealer reveals their hidden card! **")
            self.display_dealer_hand(reveal=True)

        while self.dealer_hand.calculate_value() < 17:
            print("\nDealer hits.") 
            drawn_card = self.deck.draw()
            self.dealer_hand.add_card(drawn_card)
            print(f"Dealer draws a {str(drawn_card)}.")
            self.display_dealer_hand(reveal=True)
            
            if self._is_busted(self.dealer_hand):
                return "\nDealer BUSTED!"
        
        return f"\nDealer stands at {self.dealer_hand.calculate_value()}."

    def _is_busted(self, hand: Hand) -> bool:
        return hand.calculate_value() > 21

    def compare_hand(self, hand: Hand) -> str:
        p_val = hand.calculate_value()
        d_val = self.dealer_hand.calculate_value()
        if p_val > 21: return "DEALER WINS: Player BUSTED."
        if d_val > 21: return "PLAYER WINS: Dealer BUSTED."
        if p_val == d_val: return "PUSH: It's a tie. Bet returned."
        if p_val > d_val: return "PLAYER WINS: Higher value."
        return "DEALER WINS: Higher value."

    def display_dealer_hand(self, reveal=False):
        print("\nDEALER:", self.dealer_hand.calculate_value() if reveal else "???")
        if not reveal and len(self.dealer_hand.cards) == 2:
            v = self.dealer_hand.cards[0].display_lines()
            h = [" ___ ", "|## |", "|###|", "|_##|"]
            for i in range(4): print(f"{v[i]} {h[i]}")
        else:
            print(self.dealer_hand)

    def display_player_hand(self):
        multi = len(self.player_hands) > 1
        for i, hand in enumerate(self.player_hands):
            if multi:
                label = f"HAND {i+1}"
                if i == self.active_hand_index:
                    print(f"\n--- CURRENTLY PLAYING: {label} ({hand.calculate_value()}) ---")
                else:
                    print(f"\nPLAYER {label}: {hand.calculate_value()}")
            else:
                print(f"\nPLAYER: {hand.calculate_value()}")
            print(hand)