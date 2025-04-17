def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    try:
        cooperation, rejection = 0, 0
        if len(opponent_history) == 0:
            return 0
        else:
            for i in opponent_history:

                if i == 0:
                    rejection += 1
                else:
                    cooperation += 1

        if my_history[-2:] == [1, 0]:
            return 0


        if len(opponent_history) in [i for i in range(95, 100)]:
            return 0

        if cooperation == 0 and rejection < 25:
            return 1
        elif rejection - cooperation == 21:
            return 1
        elif opponent_history[-10:] == [0,0,0,0,0,0,0,0,0,0]:
            return 1
        else:
            return 0
    except:
        return 0