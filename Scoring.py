#Gruppe 19
#Teilnehmer:
#Rose, Lennnert 222201353
#Schlüter, Theo Peter 222201541
#Schubert, Philipp 220200128
#Brinker, Mattis Paul 222200558
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
    Bewertet eine Position basierend auf der Distanz zu feindlichen Schlangenköpfen,
    unter Berücksichtigung der Anzahl sicherer Züge des Gegners.

    Args:
        pos (tuple): Zu bewertende Position (x, y).
        game_state (dict): Aktueller Spielzustand mit "you" und "board".

    Returns:
        float: Negativer Wert (-100 / n), wenn eine Kopf-Kollision mit gleichlanger oder längerer Schlange droht,
               positiver Wert (+100 / n), wenn eine Kopf-Kollision mit kürzerer Schlange möglich ist,
               geteilt durch Anzahl der sicheren Züge der gegnerischen Schlange (n).
               Falls n = 0, wird 0 zurückgegeben.
    """
    my_len = len(game_state["you"]["body"])
    score = 0

    for snake in game_state["board"]["snakes"]:
        if snake["id"] == game_state["you"]["id"]:
            continue

        enemy_head = (snake["body"][0]["x"], snake["body"][0]["y"])
        enemy_len = len(snake["body"])
        dist = manhattan_dist(pos, enemy_head)

        if dist == 1:
            
            safe_moves = 0
            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                next_pos = (enemy_head[0] + dx, enemy_head[1] + dy)
                if is_safe(next_pos, game_state):
                    safe_moves += 1

            if safe_moves == 0:
                return 0 

            if enemy_len >= my_len:
                score += -100 / safe_moves
            else:
                score += 100 / safe_moves

    return score


