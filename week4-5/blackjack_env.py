import random

class BlackjackEnv:
    def __init__(self):
        self.deck = []
        self.reset_deck()

    def reset_deck(self):
        # 6-deck shoe for statistical stationarity
        self.deck = [2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10, 11] * 4 * 6
        random.shuffle(self.deck)

    def draw(self):
        if len(self.deck) < 15: self.reset_deck()
        return self.deck.pop()

    def get_hand_value(self, hand):
        val = sum(hand)
        aces = hand.count(11)
        while val > 21 and aces:
            val -= 10
            aces -= 1
        return val

    def get_state(self, hand, d_card):
        p_sum = self.get_hand_value(hand)
        usable_ace = (hand.count(11) > 0 and (p_sum <= 21))
        is_pair = len(hand) == 2 and hand[0] == hand[1]
        return (p_sum, d_card, usable_ace, is_pair)

    def reset(self, force_player_sum=None):
        self.dealer_hand = [self.draw(), self.draw()]
        if force_player_sum == 5: 
            self.player_hand = [2, 3]
        elif force_player_sum == 21: 
            self.player_hand = [11, 10]
        else: 
            self.player_hand = [self.draw(), self.draw()]
        return self.get_state(self.player_hand, self.dealer_hand[0])

    def step(self, action):
        d_card = self.dealer_hand[0]
        if action == 1: # hit
            self.player_hand.append(self.draw())
            if self.get_hand_value(self.player_hand) > 21:
                return self.get_state(self.player_hand, d_card), -1, True
            return self.get_state(self.player_hand, d_card), 0, False
        
        elif action == 2: # double down
            self.player_hand.append(self.draw())
            p_val = self.get_hand_value(self.player_hand)
            reward = -2 if p_val > 21 else self.play_dealer(p_val) * 2
            return self.get_state(self.player_hand, d_card), reward, True
        
        elif action == 3: # split
            c1, c2 = self.player_hand[0], self.player_hand[1]
            # resolve split hands with improved proxy
            r1 = self.auto_resolve([c1, self.draw()], d_card)
            r2 = self.auto_resolve([c2, self.draw()], d_card)
            return self.get_state(self.player_hand, d_card), r1 + r2, True
        
        else: # stand
            reward = self.play_dealer(self.get_hand_value(self.player_hand))
            return self.get_state(self.player_hand, d_card), reward, True

    def auto_resolve(self, hand, d_card):
        # proxy strategy refined to match basic strategy chart
        while True:
            val = self.get_hand_value(hand)
            is_soft = (11 in hand) and (sum(hand) <= 21)
            
            if val > 21: break 

            # logic for soft totals (ace involved)
            if is_soft:
                if val <= 17: # hit soft 17 or less
                    hand.append(self.draw())
                    continue
                if val == 18 and d_card in [9, 10, 11]: # hit soft 18 vs strong dealer
                    hand.append(self.draw())
                    continue
                break # stand on soft 18+ otherwise

            # logic for hard totals
            if val >= 17: break
            if 12 <= val <= 16 and 2 <= d_card <= 6: break
            
            hand.append(self.draw())
            
        p_val = self.get_hand_value(hand)
        return -1 if p_val > 21 else self.play_dealer(p_val)

    def play_dealer(self, p_val):
        while self.get_hand_value(self.dealer_hand) < 17:
            self.dealer_hand.append(self.draw())
        d_val = self.get_hand_value(self.dealer_hand)
        if d_val > 21 or p_val > d_val: return 1
        return -1 if p_val < d_val else 0