import random
import typing
import heapq
from collections import deque
from Dead_End import dead_end_bonus
from Scoring import edge_penalty, nohead_score
from Helper import is_safe, get_new_position, freedom_score, tailchase
from Astar import get_food_move, a_star


def info() -> typing.Dict:
    return {
        "apiversion": "1",
        "author": "philipp",
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
    food_move_scores = get_food_move(game_state)

    moves = ["up", "down", "left", "right"]
    evaluated_moves = []

    for move in moves:
        new_pos = get_new_position(head, move)
        if not is_safe(new_pos, game_state):
            continue

        my_length = len(game_state["you"]["body"])
        free = freedom_score(new_pos, game_state)

        score = 0

        score += 2 * food_move_scores.get(move, 0)  # ✅ Bonus aus get_food_move
        score += 3 * nohead_score(new_pos, game_state)
        score += (free - my_length) * 3
        score += edge_penalty(new_pos, game_state)
        score += tailchase(new_pos, game_state)
        score += dead_end_bonus(move, new_pos, game_state)

        evaluated_moves.append((score, free, move))

    if evaluated_moves:
        best_move = max(evaluated_moves, key=lambda m: (m[0], m[1]))[2]
        return {"move": best_move}
    else:
        legal_moves = [
            m for m in moves if is_safe(get_new_position(head, m), game_state)
        ]
        if legal_moves:
            print("No good move. Picking any legal move.")
            return {"move": random.choice(legal_moves)}
        else:
            print(" No legal move. Going down by default.")
            return {"move": "down"}


# ---------- SERVERSTART -------------------

if __name__ == "__main__":
    from server import run_server
    run_server({
        "info": info,
        "start": start,
        "move": move,
        "end": end,
    })
