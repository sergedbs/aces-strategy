def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:

    if len(my_history) < 3:
        return [1, 0, 1][len(my_history)]

    # Analysis phase (first 20% rounds)
    if rounds and (len(my_history) < rounds // 5):
        trust_score = sum(opponent_history) / len(opponent_history)
        if (len(my_history) % 7 == 0) and (trust_score > 0.6):
            return 0  # Occasional betrayal
        return 1 if trust_score > 0.5 else 0
    else:
        # Main phase: dynamic adaptation
        recent_moves = opponent_history[-5:] if len(opponent_history) >= 5 else opponent_history
        opponent_trend = sum(recent_moves) / len(recent_moves) if recent_moves else 0.5

        if opponent_trend < 0.3:  # Aggressive opponent
            return 0 if (len(my_history) % 10 != 0) else 1  # 10% forgiveness
        elif 0.3 <= opponent_trend <= 0.7:  # Unpredictable opponent
            return 1 if ((len(my_history) * 13) % 100) < 55 else 0
        else:  # Cooperative opponent
            return 0 if (len(my_history) % 8 == 0) else 1  # 12.5% betrayal rate

