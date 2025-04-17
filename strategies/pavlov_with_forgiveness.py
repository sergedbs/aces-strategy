def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    # First cooperate
    if not my_history or not opponent_history:
        return 1

    my_last_moves = my_history[-30:]
    opp_last_moves = opponent_history[-30:]

    my_last = my_history[-1]
    opp_last = opponent_history[-1]

    # If both players made the same move in the last round, repeat that move
    # (1,1) or (0,0) -> stay
    if my_last == opp_last:
        return my_last

    # If I cooperated and the opponent defected, shift, but I might forgive with a 20% chance
    # (1,0) -> shift (0)
    if my_last == 1 and opp_last == 0:
        history_hash = hash(str(my_last_moves) + str(opp_last_moves))
        if history_hash % 5 == 0:
            return 1
        else:
            return 0

    # If my last move was a defection and the opponent cooperated, shift
    # (0,1) -> shift (1)
    return 1
