from Helper import manhattan_dist


def edge_penalty(pos, game_state):
    x, y = pos
    width = game_state["board"]["width"]
    height = game_state["board"]["height"]

    if x == 0 or x == width - 1 or y == 0 or y == height - 1:
        corners = [(0, 0), (0, height - 1), (width - 1, 0), (width - 1, height - 1)]
        min_corner_distance = min(abs(x - cx) + abs(y - cy) for (cx, cy) in corners)

        max_distance = (width + height) // 2
        penalty = -5 + (min_corner_distance / max_distance) * 5 

        return penalty

    return 0

def nohead_score(pos, game_state):
  my_len = len(game_state["you"]["body"])
  score = 0
  for snake in game_state["board"]["snakes"]:
      if snake["id"] == game_state["you"]["id"]:
          continue
      enemy_head = snake["body"][0]
      enemy_len = len(snake["body"])
      if manhattan_dist(pos, (enemy_head["x"], enemy_head["y"])) == 1:
          if enemy_len >= my_len:
              return -100
          else:
              score += 100
  return score

