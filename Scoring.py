from Helper import manhattan_dist


def edge_penalty(pos, game_state):
    """
    Berechnet eine Strafwertung, wenn sich die Schlange am Rand des Spielfelds befindet.

    Args:
        pos (tuple): Zu bewertende Position (x, y).
        game_state (dict): Aktueller Spielzustand mit "you" und "board".

    Returns:
        float: Negativer Strafwert (bis -5) basierend auf Abstand zur nächsten Ecke,
               oder 0, wenn Sie sich nicht am Rand befindet.
    """
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
    """
    Bewertet eine Position basierend auf der Distanz zu feindlichen Schlangenköpfen, zur Vermeidung von Kollisionen.

    Args:
        pos (tuple): Zu bewertende Position (x, y).
        game_state (dict):  Aktueller Spielzustand mit "you" und "board".

    Returns:
        int: Negativer Wert (-100), wenn eine Kopf-Kollision gleichlanger oder längerer Gegner möglich ist;
             positiver Wert (+100) wenn eine Kopf-Kollision mit einer kürzeren Schlange möglich ist;
             ansonsten 0.
    """
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

