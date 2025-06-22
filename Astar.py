from Helper import is_safe, manhattan_dist, get_direction, freedom_score

import heapq


def get_food_move(game_state):
    """
  Gibt ein Dictionary zurück: {'up': 5, 'left': 0, ...}
  Jede Richtung bekommt Bonuspunkte, wenn sie auf dem Weg zum Futter liegt.
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
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    return path[::-1]
