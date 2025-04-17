def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:

    defect_values = {1, 6, 7, 17, 22, 23, 26, 29, 30, 31,
                     33, 38, 39, 45, 49, 54, 55, 58, 61}

    n = len(my_history)

    if n == 0:
        return 1

    if n == 1:
        return opponent_history[0]

    if n == 2:
        if my_history[0] > opponent_history[0] and my_history[1] < opponent_history[1]:
            return 0
        else:
            return opponent_history[1]

    weights = [1, 4, 16]
    A = 0
    for i in range(3):
        points = 0
        if my_history[n - 3 + i] == 0:
            points += 1
        if opponent_history[n - 3 + i] == 0:
            points += 2
        A += weights[i] * points

    if A in defect_values:
        return 0
    else:
        return 1



