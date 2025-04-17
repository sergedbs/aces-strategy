def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    if not hasattr(strategy, "opponent_cooperation_rate"):
        strategy.opponent_cooperation_rate = 0
        strategy.last_three_moves = []
        strategy.total_rounds = rounds
        strategy.rounds_played = 0

    if opponent_history:
        strategy.opponent_cooperation_rate = sum(opponent_history) / len(opponent_history)
        strategy.last_three_moves.append(opponent_history[-1])
        if len(strategy.last_three_moves) > 3:
            strategy.last_three_moves.pop(0)

    strategy.rounds_played += 1

    if not my_history:
        return 1

    if strategy.total_rounds and strategy.rounds_played >= strategy.total_rounds - 1:
        return 0

    if strategy.opponent_cooperation_rate > 0.7:
        return 0 if hash(tuple(opponent_history)) % 10 < 8 else 1

    if strategy.opponent_cooperation_rate < 0.3:
        return 0

    if len(opponent_history) >= 3:
        if opponent_history[-3:] == [1, 0, 1] or opponent_history[-3:] == [0, 1, 0]:
            return 0

    if len(opponent_history) >= 5:
        recent_moves = opponent_history[-5:]
        if recent_moves.count(recent_moves[0]) == len(recent_moves):
            return 0

    if strategy.rounds_played % 10 == 0:
        return 1

    return opponent_history[-1] if opponent_history else 1

