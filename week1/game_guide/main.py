import sys
from blackjack import BlackJack, calculate_winnings

def print_rules():
    print("Rules:")
    print(" Try to get as close to 21 without going over.")
    print(" Kings, Queens, and Jacks are worth 10 points.")
    print(" Aces are worth 1 or 11 points.")
    print(" Cards 2 through 10 are worth their face value.")
    print(" (H)it to take another card.")
    print(" (S)tand to stop taking cards.")
    print(" (D)ouble down to increase your bet but must hit exactly one more time.")
    print(" In case of a tie (PUSH), the bet is returned to the player.")
    print(" Player Blackjack pays 1.5x the bet.")
    print(" The dealer stops hitting at 17.")
    print("-" * 40)

def main_game_loop():
    game = BlackJack()
    money = 5000
    print_rules()
    
    while money > 0:
        print(f"\n--- NEW HAND ---")
        print(f"Money: {money}")
        
        while True:
            bet_input = input(f"How much do you bet? (1-{money}, or QUIT)\n> ").strip().upper()
            if bet_input == "QUIT":
                print(f"Thanks for playing! You leave with ${money}.")
                sys.exit()
            try:
                bet = int(bet_input)
                if 1 <= bet <= money: break
                else: print("Invalid bet amount.")
            except ValueError: print("Invalid input.")

        money -= bet
        initial_result = game.start_match(bet)

        # To test split
        # from cards import Card, Rank, Suit
        # game.player_hands[0].cards = [Card(Rank.ACE, Suit.SPADES), Card(Rank.ACE, Suit.HEARTS)]
        
        if initial_result:
            print("\n--- Initial Outcome ---")
            game.display_dealer_hand(reveal=True)
            game.display_player_hand()
            outcome = initial_result
            winnings_delta = calculate_winnings(outcome, bet)
            money += bet + winnings_delta 
            print('\n' + "-" * 40)
            if "PLAYER WINS: BLACKJACK" in outcome:
                print(f"Player BLACKJACK! You won ${winnings_delta}!")
            elif winnings_delta > 0:
                print(f"You won ${winnings_delta}!")
            elif winnings_delta < 0:
                print(f"You lost ${abs(winnings_delta)}! ({outcome.split(':')[1].strip()})")
            else:
                print(f"PUSH. Bet returned.")
            print("-" * 40)
            continue 

        # --- Player's Turn ---
        while game.active_hand_index < len(game.player_hands):
            hand = game.get_active_hand()
            game.is_doubling_down = False
            is_first_play = True
            turn_active = True
            
            while turn_active:
                game.display_dealer_hand(reveal=False)
                game.display_player_hand()

                allowed_actions = "(H)it, (S)tand"
                can_double = is_first_play and (money >= hand.bet)
                can_split = is_first_play and (money >= hand.bet) and (hand.cards[0].rank == hand.cards[1].rank)
                
                if can_double: allowed_actions += ", (D)ouble down"
                if can_split: allowed_actions += ", S(P)lit"
                
                hand_label = f"Hand {game.active_hand_index + 1}" if len(game.player_hands) > 1 else "your hand"
                action = input(f"\nAction for {hand_label} ({allowed_actions})\n> ").strip().upper()
                
                if action == 'H':
                    message, game_ended = game.hit()
                    print(message)
                elif action == 'S':
                    message, game_ended = game.stand()
                    print(message)
                elif action == 'D' and can_double:
                    money -= hand.bet
                    hand.bet *= 2
                    message, game_ended = game.double_down()
                    print(message)
                elif action == 'P' and can_split:
                    money -= hand.bet
                    game.split()
                    print("Hand split!")
                    continue
                else:
                    print("Invalid action.")
                    continue

                is_first_play = False
                if game_ended or game._is_busted(hand):
                    turn_active = False
                    if len(game.player_hands) > 1 and game.active_hand_index < len(game.player_hands) - 1:
                        print(f"\nMoving to Hand {game.active_hand_index + 2}...")
            
            game.active_hand_index += 1

        # --- Dealer's Turn & Final Results ---
        if not all(game._is_busted(h) for h in game.player_hands):
            print(game.dealer_play())

        print("-" * 40)
        game.display_dealer_hand(reveal=True)
        game.display_player_hand()
        print('\n' + "-" * 40)

        for i, h in enumerate(game.player_hands):
            outcome = game.compare_hand(h)
            winnings_delta = calculate_winnings(outcome, h.bet)
            money += h.bet + winnings_delta
            
            # Use label Hand 1/2 only if a split occurred
            label = f"Hand {i+1}: " if len(game.player_hands) > 1 else ""

            if winnings_delta > 0:
                print(f"{label}You won ${winnings_delta}!")
            elif winnings_delta < 0:
                print(f"{label}You lost ${abs(winnings_delta)}!")
            else:
                print(f"{label}PUSH. Bet returned.")

        print("-" * 40)

    print("\nGame Over: You ran out of money!")

if __name__ == '__main__':
    main_game_loop()