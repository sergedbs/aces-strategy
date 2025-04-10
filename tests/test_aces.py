from __future__ import annotations

import random
from aces import strategy as aces_strategy

# Benchmark strategies
def always_cooperate(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    return 1

def always_defect(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    return 0

def tit_for_tat(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    if not my_history:
        return 1
    return opponent_history[-1]

def random_strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    return random.choice([0, 1])

# Scoring function based on the game rules.
def compute_score(my_move: int, opponent_move: int) -> tuple[int, int]:
    if my_move == 1 and opponent_move == 1:
        return 3, 3  # Both cooperate
    elif my_move == 1 and opponent_move == 0:
        return 0, 5  # I cooperate, opponent defects
    elif my_move == 0 and opponent_move == 1:
        return 5, 0  # I defect, opponent cooperates
    else:
        return 1, 1  # Both defect

# Simulate one match between two strategies over a fixed number of rounds.
def simulate_match(strategy_A, strategy_B, rounds: int = 100) -> tuple[int, int]:
    history_A = []
    history_B = []
    score_A = 0
    score_B = 0
    for round_num in range(1, rounds + 1):
        move_A = strategy_A(history_A, history_B, rounds)
        move_B = strategy_B(history_B, history_A, rounds)
        history_A.append(move_A)
        history_B.append(move_B)
        pts_A, pts_B = compute_score(move_A, move_B)
        score_A += pts_A
        score_B += pts_B
    return score_A, score_B

# Run a round-robin tournament with many trials per pairing.
def run_tournament(trials: int = 100, rounds: int = 100):
    # Define all strategies.
    strategies = {
        "Always Cooperate": always_cooperate,
        "Always Defect": always_defect,
        "Tit-for-Tat": tit_for_tat,
        "Random": random_strategy,
        "ACES": aces_strategy
    }
    names = list(strategies.keys())
    # Matrix to store list of total scores for each matchup (score for A when A plays B).
    matchup_results = {name: {opp: [] for opp in names} for name in names}
    # Also, track total scores and match count per strategy.
    total_scores = {name: 0 for name in names}
    match_count = {name: 0 for name in names}

    # For each pairing, run multiple trials.
    for name_A in names:
        for name_B in names:
            for t in range(trials):
                sA, sB = simulate_match(strategies[name_A], strategies[name_B], rounds)
                matchup_results[name_A][name_B].append(sA)
                total_scores[name_A] += sA
                match_count[name_A] += 1

    # Compute the average score for each matchup.
    average_matchup = {name: {} for name in names}
    for name in names:
        for opp in names:
            scores = matchup_results[name][opp]
            average_matchup[name][opp] = sum(scores) / len(scores) if scores else 0

    # Build leaderboard: total score and average score per match.
    leaderboard = {}
    for name in names:
        leaderboard[name] = {
            "total_score": total_scores[name],
            "avg_score": total_scores[name] / match_count[name] if match_count[name] > 0 else 0
        }
    # Sort leaderboard by average score per match (descending).
    sorted_leaderboard = sorted(leaderboard.items(), key=lambda x: x[1]["avg_score"], reverse=True)
    return average_matchup, leaderboard, sorted_leaderboard

def print_results(average_matchup, leaderboard, sorted_leaderboard):
    names = list(average_matchup.keys())
    print("\n=== Average Total Score Matrix (per match) ===")
    header = "Strategy".ljust(20) + "".join(name.ljust(15) for name in names)
    print(header)
    for name in names:
        row = name.ljust(20)
        for opp in names:
            row += f"{average_matchup[name][opp]:.2f}".ljust(15)
        print(row)
    print("\n=== Leaderboard ===")
    print("Strategy".ljust(20) + "Total Score".ljust(15) + "Avg Score per Match")
    for name, scores in sorted_leaderboard:
        print(name.ljust(20) + f"{scores['total_score']:.2f}".ljust(15) + f"{scores['avg_score']:.2f}")

if __name__ == "__main__":
    # Run tournament: 100 trials per matchup, 100 rounds each.
    avg_matchup, leaderboard, sorted_lb = run_tournament(trials=200, rounds=200)
    print_results(avg_matchup, leaderboard, sorted_lb)
