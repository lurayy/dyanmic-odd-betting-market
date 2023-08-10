class BettingGame:

    def __init__(self, outcome):
        self.outcome = outcome
        self.players = {}

    def place_bet(self, player_name, amount, bet_outcome):
        if player_name in self.players:
            self.players[player_name].append((amount, bet_outcome))
        else:
            self.players[player_name] = [(amount, bet_outcome)]

    def calculate_payouts(self):
        total_pot = 0
        winning_pot = 0

        for bets in self.players.values():
            for amount, bet_outcome in bets:
                total_pot += amount
                if bet_outcome == self.outcome:
                    winning_pot += amount

        if winning_pot == 0:
            return {player_name: 0 for player_name in self.players}

        payouts = {}
        for player_name, bets in self.players.items():
            total_player_amount = sum(amount for amount, _ in bets)
            if self.players[player_name][0][
                    1] == self.outcome:  # Check the first bet outcome
                player_share = total_player_amount / winning_pot
                player_payout = player_share * total_pot
                payouts[player_name] = player_payout
            else:
                payouts[player_name] = 0  # Losing players get no payout

        return payouts


def main():
    outcome = input("Enter the winning outcome (0 or 1): ")
    try:
        outcome = int(outcome)
        if outcome not in [0, 1]:
            raise ValueError()
    except ValueError:
        print("Invalid outcome entered. Please enter 0 or 1.")
        return

    game = BettingGame(outcome)

    while True:
        player_name = input("Enter player name (or 'exit' to finish): ")
        if player_name.lower() == 'exit':
            break

        try:
            amount = float(input("Enter bet amount: "))
            bet_outcome = int(input("Enter bet outcome (0 or 1): "))
            if bet_outcome not in [0, 1]:
                raise ValueError()

            game.place_bet(player_name, amount, bet_outcome)
        except ValueError:
            print("Invalid input. Please enter valid values.")

    payouts = game.calculate_payouts()
    print("\nPayouts:")
    for player_name, payout in payouts.items():
        print(f"{player_name}: {payout:.2f}")


if __name__ == "__main__":
    main()
