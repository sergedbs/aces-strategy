def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
    ZODIAC_SIGNS = [
        'ARIES', 'TAURUS', 'GEMINI', 'CANCER', 'LEO', 'VIRGO', 
        'LIBRA', 'SCORPIO', 'SAGITTARIUS', 'CAPRICORN', 'AQUARIUS', 'PISCES'
    ]
    
    RULES_OF_DESTINY = ['ELEMENT', 'DAY_AND_NIGHT_RULERSHIP', 'HEMISPHERE']
    
    ELEMENT_RULE = {
        'FIRE': ['ARIES', 'LEO', 'SAGITTARIUS'],
        'EARTH': ['TAURUS', 'VIRGO', 'CAPRICORN'],
        'AIR': ['GEMINI', 'LIBRA', 'AQUARIUS'],
        'WATER': ['CANCER', 'SCORPIO', 'PISCES']
    }
    
    DAY_AND_NIGHT_RULERSHIP = {
        'DAY': ['LEO', 'SAGITTARIUS', 'AQUARIUS', 'ARIES', 'LIBRA', 'GEMINI'],
        'NIGHT': ['CANCER', 'PISCES', 'CAPRICORN', 'SCORPIO', 'TAURUS', 'VIRGO']
    }
    
    HEMISPHERE_RULE = {
        'SPRING': ['ARIES', 'TAURUS', 'GEMINI'],
        'SUMMER': ['CANCER', 'LEO', 'VIRGO'],
        'FALL': ['LIBRA', 'SCORPIO', 'SAGITTARIUS'],
        'WINTER': ['CAPRICORN', 'AQUARIUS', 'PISCES']
    }
    
    PREDICTION_RESULT = 1
        
    player_destiny = sum(my_history)
    player_rule_of_destiny = RULES_OF_DESTINY[player_destiny % 3]
      
    opponent_destiny = sum(opponent_history)
    opponent_sign = ZODIAC_SIGNS[opponent_destiny % 12]
    
    if player_rule_of_destiny == 'ELEMENT':
        opponent_element = 'FIRE'
        
        for element in ELEMENT_RULE:
            if opponent_sign in ELEMENT_RULE[element]:
                opponent_element = element
        
        if opponent_element in ['FIRE', 'AIR']:
            PREDICTION_RESULT = 1
        else:
            PREDICTION_RESULT = 0
            
    elif player_rule_of_destiny == 'DAY_AND_NIGHT_RULERSHIP':
        opponent_time = 'DAY'
        
        for time in DAY_AND_NIGHT_RULERSHIP:
            if opponent_sign in DAY_AND_NIGHT_RULERSHIP[time]:
                opponent_time = time
                
        if opponent_time == 'DAY':
            PREDICTION_RESULT = 1
        else:
            PREDICTION_RESULT = 0
            
    elif player_rule_of_destiny == 'HEMISPHERE':
        opponent_season = 'SPRING'
        
        for season in HEMISPHERE_RULE:
            if opponent_sign in HEMISPHERE_RULE[season]:
                opponent_season = season
                
        if opponent_season in ['SPRING', 'SUMMER']:
            PREDICTION_RESULT = 1
        else:
            PREDICTION_RESULT = 0
        
    return PREDICTION_RESULT
