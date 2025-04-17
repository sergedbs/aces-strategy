def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    if len(my_history) == 0:
        return 1

    cooperation_count = opponent_history.count(1)
    defection_count = opponent_history.count(0)
    
    if len(my_history) < 5:
        return 1 if cooperation_count >= defection_count else 0

    if defection_count > cooperation_count:
        return 0
    elif cooperation_count > defection_count:
        return 1
    else:
        return 1 if my_history[-1] == 0 else 0
