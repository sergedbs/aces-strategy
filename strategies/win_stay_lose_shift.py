def strategy(my_history: 'list[int]', opponent_history: 'list[int]', rounds: 'int | None') -> int:
    """
    Win-Stay, Lose-Shift (Pavlov) strategy.
    1) If this is the first move, cooperate.
    2) Otherwise, calculate your own payoff from the last round:
       - If that payoff is 3 or 5, repeat your last move.
       - If that payoff is 0 or 1, switch your last move.
    """
    if len(my_history) == 0:
        return 1

    my_last_move = my_history[-1]
    opp_last_move = opponent_history[-1]

    if my_last_move == 0 and opp_last_move == 0:
        my_payoff = 1
    elif my_last_move == 0 and opp_last_move == 1:
        my_payoff = 5
    elif my_last_move == 1 and opp_last_move == 0:
        my_payoff = 0
    else:  # my_last_move == 1 and opp_last_move == 1
        my_payoff = 3

    if my_payoff in (3, 5):
        return my_last_move
    else:
        return 1 - my_last_move