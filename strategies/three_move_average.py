def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    if len(opponent_history)<3:
        if len(opponent_history)<2:
            return 1
        if opponent_history[0] == opponent_history[1]:
            return  opponent_history[0]
        else:
            return 1
    if opponent_history[-1] == opponent_history[-2]:
        return  opponent_history[-1]
    else:
        return opponent_history[-3]