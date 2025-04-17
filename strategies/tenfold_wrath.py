def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    if my_history is None:
        my_history = []
    if opponent_history is None:
        opponent_history = []

    if len(my_history) == 0:
        strategy.defection_count = 0
        strategy.defection_mode = False
        strategy.defection_streak = 0

    if len(opponent_history) > 0 and opponent_history[-1] == 0:
        strategy.defection_count += 1

    if not strategy.defection_mode and strategy.defection_count >= 2:
        strategy.defection_mode = True
        strategy.defection_streak = 0

    if strategy.defection_mode:
        strategy.defection_streak += 1
        if strategy.defection_streak <= 10:
            return 0
        if opponent_history[-1] == 1:
            strategy.defection_mode = False
            strategy.defection_streak = 0
            strategy.defection_count = 0
            return 1
        else:
            return 0

    return 1