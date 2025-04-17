def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    if my_history is None:
        my_history = []
    if opponent_history is None:
        opponent_history = []
    if len(my_history) == 0:
        strategy.last_fresh_start = 0
    if len(my_history) <= 5:
        return opponent_history[-1] if len(opponent_history) != 0 else 1
    if rounds is not None and rounds - len(my_history) <= 2:
        return 0

    recent_opponent_moves = opponent_history[-5:]
    cooperation = recent_opponent_moves.count(1)
    defection = recent_opponent_moves.count(0)

    youre_bad = defection > cooperation

    you_get_a_fresh_start = (
            (recent_opponent_moves[-1] != 0 and recent_opponent_moves[-2] != 1)
            and len(my_history) - strategy.last_fresh_start >= 20
            and (rounds is None or rounds - len(my_history) > 10)
    )

    if you_get_a_fresh_start:
        strategy.last_fresh_start = len(my_history)
        return 1

    if youre_bad:
        return 0

    return opponent_history[-1]
