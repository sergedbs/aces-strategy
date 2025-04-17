def strategy(my_history, opponent_history, rounds):
    seed = len(my_history) + sum(opponent_history)
    return (seed * 5144013 + 22310311) % 2