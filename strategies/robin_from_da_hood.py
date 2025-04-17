def strategy(my_history: list[int], opponent_history: list[int], rounds: int | None) -> int:
  total_rounds = len(my_history)
  my_zeros = total_rounds-sum(my_history)
  opp_zeros = total_rounds-sum(opponent_history)

  last_three_ones = len(opponent_history)>3 and opponent_history[-1] == opponent_history[-2] == opponent_history[-3] == 1
  dynamic_gap = 0
  dynamic_gap_less = dynamic_gap + total_rounds//4
  if last_three_ones:
    return 1
  if opp_zeros >= my_zeros+dynamic_gap or opp_zeros < my_zeros -dynamic_gap_less:
    return 0  
  return 1