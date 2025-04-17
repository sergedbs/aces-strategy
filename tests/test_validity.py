import random

# -------------------- PASTE YOUR STRATEGY FUNCTION HERE --------------------
from aces import strategy

from aces.aces_round_3 import strategy_round_3
# ------------------ DO NOT MODIFY ANY OF THE NEXT CODE ---------------------

def random_opponent_strategy():
    """Returns a random move: 0 (defect) or 1 (cooperate)."""
    return random.choice([0, 1])

def compute_score(my_move, opponent_move):
    """Computes the score based on the game rules."""
    if my_move == 1 and opponent_move == 1:
        return 3, 3  # Both cooperate
    elif my_move == 1 and opponent_move == 0:
        return 0, 5  # Player cooperates, opponent defects
    elif my_move == 0 and opponent_move == 1:
        return 5, 0  # Player defects, opponent cooperates
    else:
        return 1, 1  # Both defect

def test_round_1(rounds: int = 100):
    """Tests the strategy in Round 1 (Fixed Rounds, Random Opponent)."""
    my_history = []
    opponent_history = []
    player_score = 0
    opponent_score = 0

    print("\n--- Testing Round 1 ---")
    for round_num in range(1, rounds + 1):
        my_move = strategy(my_history, opponent_history, rounds)
        opponent_move = random_opponent_strategy()

        my_history.append(my_move)
        opponent_history.append(opponent_move)

        # Update scores
        my_points, opp_points = compute_score(my_move, opponent_move)
        player_score += my_points
        opponent_score += opp_points

        #print(f"Round {round_num}: Player -> {my_move}, Opponent -> {opponent_move}")

    print("\nFinal History (Round 1):")
    print("Player:   ", my_history)
    print("Opponent: ", opponent_history)
    print(f"Final Score - Player: {player_score}, Opponent: {opponent_score}")

def test_round_2():
    """Tests the strategy in Round 2 (Unknown Rounds, Random Opponent)."""
    my_history = []
    opponent_history = []
    player_score = 0
    opponent_score = 0
    rounds_played = random.randint(100, 200)  # Unknown number of rounds (at least 50)

    print("\n--- Testing Round 2 ---")
    for round_num in range(1, rounds_played + 1):
        my_move = strategy(my_history, opponent_history, None)
        opponent_move = random_opponent_strategy()

        my_history.append(my_move)
        opponent_history.append(opponent_move)

        # Update scores
        my_points, opp_points = compute_score(my_move, opponent_move)
        player_score += my_points
        opponent_score += opp_points

        #print(f"Round {round_num}: Player -> {my_move}, Opponent -> {opponent_move}")

    print("\nFinal History (Round 2):")
    print("Player:   ", my_history)
    print("Opponent: ", opponent_history)
    print(f"Final Score - Player: {player_score}, Opponent: {opponent_score}")

def test_round_3():
    """Tests the strategy in Round 3 (1000 rounds, opponent selection, dynamic history)."""
    num_opponents = 6
    rounds_played = 0

    # Initialize empty history dictionaries
    my_history = {i: [] for i in range(1, num_opponents + 1)}
    opponents_history = {i: [] for i in range(1, num_opponents + 1)}
    scores = {i: 0 for i in range(1, num_opponents + 1)}  # Track individual scores

    # Start with a random opponent
    current_opponent = random.choice(list(my_history.keys()))

    print("\n--- Testing Round 3 ---")
    for _ in range(1000):
        if len(my_history[current_opponent]) >= 200:
            # Find an opponent who has played less than 200 rounds
            available_opponents = [i for i in my_history if len(my_history[i]) < 200]
            if not available_opponents:
                break  # Stop if all opponents have reached 200 rounds
            current_opponent = random.choice(available_opponents)

        # Get player's move and next opponent choice
        move, next_opponent = strategy_round_3(current_opponent, my_history, opponents_history)
        opponent_move = random_opponent_strategy()  # Opponent moves randomly

        # Store moves in history
        my_history[current_opponent].append(move)
        opponents_history[current_opponent].append(opponent_move)

        # Update scores
        my_points, opp_points = compute_score(move, opponent_move)
        scores[current_opponent] += my_points

        # Print round result
        rounds_played += 1
        #print(f"Round {rounds_played}: vs Opponent {current_opponent} | Player -> {move}, Opponent -> {opponent_move} | Next Opponent: {next_opponent}")

        # Update next opponent
        current_opponent = next_opponent if next_opponent in my_history else random.choice(list(my_history.keys()))

    # Print final statistics
    print("\n--- Final Results (Round 3) ---")
    for opponent, history in my_history.items():
        print(f"Opponent {opponent}: Played {len(history)} rounds, Score: {scores[opponent]}")


# Run all tests and print final scores

test_round_1(100)  # Fixed 100 rounds
test_round_2()     # Unknown rounds
test_round_3()     # Adaptive opponent selection