import random
import typing
import heapq
from collections import deque

def info() -> typing.Dict:
    return {
        "apiversion": "1",
        "author": "philipp-ai",
        "color": "#00ff00",
        "head": "beluga",
        "tail": "bolt",
    }

def start(game_state: typing.Dict):
    print("GAME START")

def end(game_state: typing.Dict):
    print("GAME OVER")

def move(game_state: typing.Dict) -> typing.Dict:
    head = game_state["you"]["body"][0]
    pos = (head["x"], head["y"])

    # 🍎 Futterpfad wenn du der Schnellste bist
    move_to_food = get_food_move(game_state)
    if move_to_food:
        print(f"🍎 Going for food: {move_to_food}")
        return {"move": move_to_food}

    moves = ["up", "down", "left", "right"]
    evaluated_moves = []

    for move in moves:
        new_pos = get_new_position(head, move)
        if not is_safe(new_pos, game_state):
            continue

        free = freedom_score(new_pos, game_state)
        score = 0
        score += get_food_score(new_pos, game_state)
        score += 3 * nohead_score(new_pos, game_state)
        score += free * 2
        score += edge_penalty(new_pos, game_state)

        if move_is_trap(new_pos, game_state):
            score -= 30  # Malus statt Ausschluss

        my_tail = game_state["you"]["body"][-1]
        if manhattan_distance_xy(new_pos, (my_tail["x"], my_tail["y"])) == 0:
            score += 5

        evaluated_moves.append((score, free, move))

    # 🧠 Auswahllogik
    if len(game_state["board"]["snakes"]) == 2:
        print("🎯 Trap mode activated (1v1)")
        trap_move = trap(game_state)
        if trap_move:
            return {"move": trap_move}

    if evaluated_moves:
        best_move = max(evaluated_moves, key=lambda m: (m[0], m[1]))[2]
        return {"move": best_move}
    else:
        legal_moves = [m for m in moves if is_safe(get_new_position(head, m), game_state)]
        if legal_moves:
            print("😬 No good move. Picking any legal move.")
            return {"move": random.choice(legal_moves)}
        else:
            print("☠️ No legal move. Going down by default.")
            return {"move": "down"}

# ---------- HEURISTIK -------------------

def get_food_move(game_state):
    head = game_state["you"]["body"][0]
    pos = (head["x"], head["y"])
    food_list = game_state["board"]["food"]

    if not food_list:
        return None

    sorted_food = sorted(food_list, key=lambda f: manhattan_distance_xy(pos, (f["x"], f["y"])))

    for food in sorted_food:
        goal = (food["x"], food["y"])
        path = a_star(game_state, pos, goal)

        if path and len(path) > 0:
            my_distance = len(path)
            if getfoodenemies(food, my_distance, game_state):
                continue
            if freedom_score(goal, game_state) < 6:
                continue
            return get_direction(pos, path[0])

    return None

def get_food_score(pos, game_state):
    food_list = game_state["board"]["food"]
    if not food_list:
        return 0

    closest_food = min(food_list, key=lambda f: manhattan_distance_xy(pos, (f["x"], f["y"])))
    my_path = a_star(game_state, pos, (closest_food["x"], closest_food["y"]))
    if not my_path:
        return 0

    my_distance = len(my_path)
    if getfoodenemies(closest_food, my_distance, game_state):
        return 0

    return max(20 - my_distance, 1)

def getfoodenemies(food, my_distance, game_state):
    food_pos = (food["x"], food["y"])
    for snake in game_state["board"]["snakes"]:
        if snake["id"] == game_state["you"]["id"]:
            continue
        enemy_head = snake["body"][0]
        path = a_star(game_state, (enemy_head["x"], enemy_head["y"]), food_pos)
        if path and len(path) <= my_distance:
            return True
    return False

def move_is_trap(pos, game_state):
    return freedom_score(pos, game_state) < 10

def trap(game_state):
    head = game_state["you"]["body"][0]
    enemy = [s for s in game_state["board"]["snakes"] if s["id"] != game_state["you"]["id"]][0]
    enemy_head = enemy["body"][0]
    moves = ["up", "down", "left", "right"]
    best_move = None
    best_score = float("-inf")

    for move in moves:
        new_pos = get_new_position(head, move)
        if not is_safe(new_pos, game_state):
            continue

        enemy_freedom = freedom_score((enemy_head["x"], enemy_head["y"]), game_state)
        score = 0
        score += freedom_score(new_pos, game_state)
        score += -manhattan_distance_xy(new_pos, (enemy_head["x"], enemy_head["y"]))
        score += edge_penalty(new_pos, game_state)
        score += max(0, 10 - enemy_freedom)

        if score > best_score:
            best_score = score
            best_move = move

    return best_move

def edge_penalty(pos, game_state):
    x, y = pos
    width = game_state["board"]["width"]
    height = game_state["board"]["height"]
    if x == 0 or x == width - 1 or y == 0 or y == height - 1:
        return -5
    if x == 1 or x == width - 2 or y == 1 or y == height - 2:
        return -2
    return 0

def nohead_score(pos, game_state):
    my_len = len(game_state["you"]["body"])
    score = 0
    for snake in game_state["board"]["snakes"]:
        if snake["id"] == game_state["you"]["id"]:
            continue
        enemy_head = snake["body"][0]
        enemy_len = len(snake["body"])
        if manhattan_distance_xy(pos, (enemy_head["x"], enemy_head["y"])) == 1:
            if enemy_len >= my_len:
                return -100
            else:
                score += 100
    return score

def freedom_score(pos, game_state):
    visited = set()
    queue = deque([pos])
    count = 0
    while queue and count < 50:
        x, y = queue.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        count += 1
        for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            nx, ny = x+dx, y+dy
            if is_future_safe((nx, ny), game_state):
                queue.append((nx, ny))
    return count

def is_future_safe(pos, game_state):
    x, y = pos
    width = game_state["board"]["width"]
    height = game_state["board"]["height"]
    if not (0 <= x < width and 0 <= y < height):
        return False
    for snake in game_state["board"]["snakes"]:
        body = snake["body"]
        segments = body[:-1]
        for part in segments:
            if part["x"] == x and part["y"] == y:
                return False
        tail = body[-1]
        if tail["x"] == x and tail["y"] == y:
            return True
    return True

# ---------- A* PATHFINDING -------------------

def a_star(game_state, start, goal):
    open_set = [(0, start)]
    came_from = {}
    g_score = {start: 0}
    while open_set:
        _, current = heapq.heappop(open_set)
        if current == goal:
            return reconstruct_path(came_from, current)
        for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
            neighbor = (current[0]+dx, current[1]+dy)
            if not is_safe(neighbor, game_state):
                continue
            tentative_g = g_score[current] + 1
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f = tentative_g + manhattan_distance_xy(neighbor, goal)
                heapq.heappush(open_set, (f, neighbor))
    return None

def reconstruct_path(came_from, current):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
    return path[::-1]

# ---------- HILFSFUNKTIONEN -------------------

def get_new_position(pos, move):
    x, y = pos["x"], pos["y"]
    return {
        "up": (x, y + 1),
        "down": (x, y - 1),
        "left": (x - 1, y),
        "right": (x + 1, y),
    }[move]

def get_direction(start, end):
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    if dx == 1: return "right"
    if dx == -1: return "left"
    if dy == 1: return "up"
    if dy == -1: return "down"
    return "down"

def manhattan_distance_xy(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])

def is_safe(pos, game_state):
    x, y = pos
    if not (0 <= x < game_state["board"]["width"] and 0 <= y < game_state["board"]["height"]):
        return False
    for snake in game_state["board"]["snakes"]:
        body = snake["body"]
        segments = body[:-1] if snake["id"] == game_state["you"]["id"] else body
        for part in segments:
            if part["x"] == x and part["y"] == y:
                return False
    return True

# ---------- SERVERSTART -------------------

if __name__ == "__main__":
    from server import run_server
    run_server({
        "info": info,
        "start": start,
        "move": move,
        "end": end,
    })
