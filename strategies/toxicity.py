def strategy(my_history, opponent_history, rounds=None):
    round_num = len(my_history)
    def is_toxic(opponent_history):
        return opponent_history[:5].count(0) >= 3

    def is_fibonacci(n):
        a, b = 0, 1
        while b < n:
            a, b = b, a + b
        return b == n

    if round_num == 0:
        return 1

    toxic = is_toxic(opponent_history)

    if toxic:
        if round_num >= 51:
            return 0
        elif is_fibonacci(round_num):
            return 0
        elif round_num % 6 == 0:
            return 1
        elif opponent_history[-1] == 0:
            return 0
        else:
            return 1
    else:
        if opponent_history[-1] == 0:
            if round_num % 7 == 0:
                return 1
            else:
                return 0
        else:
            return 1
