from Helper import is_safe, manhattan_dist, get_direction, freedom_score

import heapq


def get_food_move(game_state):
    """
    get_food_move bewertet mögliche Züge (Richtungen), um Futter auf dem Spielfeld zu erreichen.
    
    Es wird geprüft:
    1. Ob ein Pfad zu einem Futter existiert.
    2. Ob ein Gegner früher beim Futter sein könnte.
    3. Ob am Ziel genügend Bewegungsfreiheit gegeben ist.

    Gibt ein Dictionary mit Punktwerten für Richtungen zurück (z.B. {'up': 5, 'right': 3}).
    Höhere Werte deuten auf bessere Züge in Richtung des Futters hin.

    Args:
        game_state (dict): Der aktuelle Spielzustand.

    Returns:
        dict: Bewertungen der vier Richtungen ('up', 'down', 'left', 'right').
    """
    head = game_state["you"]["body"][0]
    pos = (head["x"], head["y"])
    food_list = game_state["board"]["food"]
    if not food_list:
        return {}

    move_scores = {}
    sorted_food = sorted(food_list,
                         key=lambda f: manhattan_dist(pos, (f["x"], f["y"])))

    for food in sorted_food:
        goal = (food["x"], food["y"])
        path = a_star(game_state, pos, goal)
        if not path or len(path) == 0:
            continue

        my_distance = len(path)
        if get_food_enemies(food, my_distance, game_state):
            continue
        if freedom_score(goal, game_state) < 6:
            continue

        next_step = path[0]
        direction = get_direction(pos, next_step)
        score = max(20 - my_distance, 1)
        move_scores[direction] = score
        print(move_scores)
    return move_scores


def get_food_enemies(food, my_distance, game_state):
    """
    get_food_enemies prüft 2. der get_food_move Funktion, sprich ob andere 
    Battlesnakes schneller oder gleich Schnell am Futter sein könnten. 

    Args:
        food (dict): Die Position eines bestimmten Futters.
        my_distance (int): Die Länge des Pfads der eigenen Schlange zum Futter.
        game_state (dict): Der aktuelle Spielzustand.

    Returns:
        bool: True, wenn ein Gegner voraussichtlich schneller beim Futter sein ist.
    """
    food_pos = (food["x"], food["y"])
    for snake in game_state["board"]["snakes"]:
        if snake["id"] == game_state["you"]["id"]:
            continue
        enemy_head = snake["body"][0]
        path = a_star(game_state, (enemy_head["x"], enemy_head["y"]), food_pos)
        if path and len(path) < my_distance:
            return True
    return False


def a_star(game_state, start, goal):
    """
    Führt eine A*-Pfadsuche von einer Startposition zu einem Ziel durch.

    Berücksichtigt dabei Spielfeldgrenzen und gefährliche Positionen, indem die Funktion `is_safe` genutzt wird.

    Args:
        game_state (dict): Der aktuelle Spielzustand.
        start (tuple): Startposition (a, b).
        goal (tuple): Zielposition (x, y).

    Returns:
        list: Eine Liste von Positionen [(x1, y1), (x2, y2), ...], die den Pfad darstellen.
              Gibt None zurück, falls kein Pfad zum Ziel gefunden wird.
    """
    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            return reconstruct_path(came_from, current)
        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)
            if not is_safe(neighbor, game_state):
                continue
            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + manhattan_dist(neighbor, goal)
                heapq.heappush(open_set, (f, neighbor))
    return None


def reconstruct_path(came_from, current):
    """
    Rekonstruiert einen Pfad, von einer Zielposition ausgehend, zurück zum Startpunkt.

    Args:
        came_from (dict): Mapping von jeder, um das Futter zu erreichen, theoretisch besuchten Position auf ihre Vorgängerposition.
        current (tuple): Die Endposition des Pfads, die Position, an der sich unser Schlangen Kopf momentan befindet.

    Returns:
        list: Der rekonstruierte Pfad als Liste von Positionen [(x1, y1), (x2, y2), ...] (vom Start, bis zum Ziel).
    """
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    return path[::-1]
