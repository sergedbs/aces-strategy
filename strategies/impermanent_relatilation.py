
def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    #print("my history:      ", my_history)
    #print("opps history:    " , opponent_history)
    #print()
    lenl = len(my_history)-1
    if lenl < 0:
        return 1
    if rounds != None:
        if lenl == rounds-2:
            return 0
    if my_history[lenl] == 0 or opponent_history[lenl] == 0:
        seed = 0
        for n in range(lenl):
            seed += (2**n) * my_history[n]
        rand = (1664525*seed + 1013904223)%2**32
        forgive = rand % 100 > 80

        if forgive:
            #print(f"forgave, {rand}, {seed}")
            return 1
        #print(f"didn't forgive, {rand}, {seed}")
        return 0

    return 1
