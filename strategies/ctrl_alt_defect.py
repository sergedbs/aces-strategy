def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    # First move cooperation
    if len(my_history) == 0:
        return 1

    if rounds is not None and len(my_history) == rounds - 1:
        return 0
    
    def is_tit_for_tat(my_hist, opp_hist):
        if len(opp_hist) < 3 or opp_hist[0] != 1:
            return False
        matches = 0
        for i in range(1, len(my_hist)):
            if opp_hist[i] == my_hist[i - 1]:
                matches += 1
        return matches >= (len(my_hist) - 1) * 0.9
    
    def is_random_strategy(opp_hist):
        if len(opp_hist) < 20: 
            return False
        ones = opp_hist.count(1)
        proportion = ones / len(opp_hist)
        return 0.4 <= proportion <= 0.6
    
    def detect_exploitation_pattern(my_hist, opp_hist):
        """Detect if opponent exploits cooperation"""
        if len(my_hist) < 10:
            return False
            
        defect_after_coop = 0
        coop_count = 0
        
        for i in range(len(my_hist) - 1):
            if my_hist[i] == 1:
                coop_count += 1
                if opp_hist[i+1] == 0:
                    defect_after_coop += 1

        return coop_count > 0 and defect_after_coop / coop_count > 0.6
    
    def detect_pattern(hist, length=3):
        """Check if there's a repeating pattern of given length"""
        if len(hist) < length * 2:
            return False, None
            
        for i in range(len(hist) - length * 2 + 1):
            pattern = hist[i:i+length]
            next_seq = hist[i+length:i+length*2]
            if pattern == next_seq:
                return True, pattern
        return False, None

    if is_tit_for_tat(my_history, opponent_history):
        return 1

    if is_random_strategy(opponent_history):
        return 0

    if detect_exploitation_pattern(my_history, opponent_history):
        return 0

    has_pattern, pattern = detect_pattern(opponent_history, 3)
    if has_pattern and pattern:
        next_predicted = pattern[len(my_history) % len(pattern)]
        return 1 if next_predicted == 1 else 0

    if len(my_history) >= 2:
        if all(move == 0 for move in my_history[-2:]) and all(move == 0 for move in opponent_history[-2:]):
            return 1

    recent_window = min(10, len(opponent_history))
    recent_coop_rate = opponent_history[-recent_window:].count(1) / recent_window

    if recent_coop_rate > 0.7:
        return 1

    if recent_coop_rate < 0.3:
        return 0

    if opponent_history[-1] == 1:
        return 1
    else:
        import random
        return 1 if random.random() < 0.2 else 0