def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    cycle_length = 6
    current_round = len(my_history) + 1

    # endgame: if total rounds are known and this is the final round, defect
    if rounds is not None and current_round == rounds:
        return 0

    # early game: during the first cycle, always cooperate
    if len(my_history) < cycle_length:
        return 1

    # determine current position in the cycle
    cycle_position = current_round % cycle_length
    if cycle_position == 0:
        cycle_position = cycle_length

    # planned move: defect on the last round of every cycle
    if cycle_position == cycle_length:
        return 0

    # if there's a full previous cycle, check the opponent's cooperation rate
    if len(opponent_history) >= cycle_length:
        last_cycle = opponent_history[-cycle_length:]
        # punish: if opponent cooperated fewer than 3 times in the last cycle, defect
        if sum(last_cycle) < 3:
            return 0

    # default action: cooperate
    return 1
