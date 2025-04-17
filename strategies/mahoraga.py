def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    if len(my_history) == 0:
        return 1

    if rounds is not None and len(my_history) == rounds - 1:
        return 0 

    def is_tit_for_tat(my_hist, opp_hist):
        if len(opp_hist) == 0 or opp_hist[0] != 1:
            return False
        for i in range(1, len(my_hist)):
            if opp_hist[i] != my_hist[i - 1]:
                return False
        return True

    def is_random(opp_hist, my_hist):
        if len(opp_hist) < 15:
            return False

        ones = opp_hist.count(1)
        proportion = ones / len(opp_hist)

        if not (0.45 <= proportion <= 0.55):
            return False

        if is_tit_for_tat(my_hist, opp_hist):
            return False
        return True
    
    if is_tit_for_tat(my_history, opponent_history):
        return 1
    
    if is_random(opponent_history, my_history):
        return 0

    def check_coop_rate(my_history, opponent_history):
        count_aux = 0
        count=0
        
        for i in range(min(len(my_history),25) - 2):
            my_subarray = my_history[i:i+3]
            opp_subarray = opponent_history[i:i+3]
            
            coop_rate = my_subarray.count(1) / len(my_subarray)
            
            if coop_rate > 0.8 and opp_subarray[-1] == 0 and opp_subarray[-2]:
                count_aux += 1 
                
                if count_aux >= 2:
                    count+=1
                    count_aux=0
                if count >= 2:
                    return True
                    
        return False

    if check_coop_rate(my_history, opponent_history):
        return 0
        
    if len(my_history) > 6:
        for i in range(len(opponent_history) - 6):
            last_6_opponent = opponent_history[i:i+6]
            last_6_my = my_history[i:i+6]
            if all(move == 0 for move in last_6_opponent) and last_6_my.count(1) >= 2:
                return 0
            
    if len(my_history) >= 1:
        my_last = my_history[-1]
        their_last = opponent_history[-1]

        if my_last == 0 and their_last == 0:
            return 1 
        elif my_last == their_last:
            return my_last  
        else:
            return 0 
    return 0