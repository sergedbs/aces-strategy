import time
import random

from aces import strategy

# check execution time

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

start_time = time.time_ns()

# Test the strategy with a random opponent

def test_strategy(rounds: int = 100):
    """Tests the strategy with a random opponent."""
    my_history = []
    opponent_history = []
    player_score = 0
    opponent_score = 0

    for round_num in range(1, rounds + 1):
        my_move = strategy(my_history, opponent_history, rounds)
        opponent_move = random.randint(0, 1)  # Random move for the opponent

        my_history.append(my_move)
        opponent_history.append(opponent_move)

        # Update scores
        my_points, opp_points = compute_score(my_move, opponent_move)
        player_score += my_points
        opponent_score += opp_points

    print("\nFinal History:")
    print("Player:   ", my_history)
    print("Opponent: ", opponent_history)
    print(f"Final Score - Player: {player_score}, Opponent: {opponent_score}")
    print(f"Execution Time: {(time.time_ns() - start_time) / 1_000_000} ms")


# Run the test
test_strategy(1000)
