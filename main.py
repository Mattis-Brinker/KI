import random
import typing
import heapq
from collections import deque
from Dead_End import dead_end_bonus
from Scoring import edge_penalty, nohead_score
from Helper import is_safe, get_new_position, freedom_score, tailchase
from Astar import get_food_move, a_star


def info() -> typing.Dict:
    """
    Gibt Meta-Informationen über die eigene Battlesnake zurück, damit unsere Schlange immer identifiziert werden kann.

    Diese Informationen werden beim Start des Spiels vom Server abgefragt.

    Returns:
        dict: Informationen über Autor, API-Version, Farbe, Kopf- und Schwanztyp.
    """
    return {
        "apiversion": "1",
        "author": "philipp",
        "color": "#00ff00",
        "head": "beluga",
        "tail": "bolt",
    }


def start(game_state: typing.Dict):
    """
    Wird zu Beginn eines Spiels einmalig aufgerufen.
    Gibt "GAME START" aus. 
    Args:
        game_state (dict): Der initiale Spielzustand.
    """
    print("GAME START")


def end(game_state: typing.Dict):
    """
    Wird nach Spielende einmalig aufgerufen.
    Gibt "GAME OVER" aus. 

    Args:
        game_state (dict): Der letzte bekannte Spielzustand.
    """
    print("GAME OVER")


def move(game_state: typing.Dict) -> typing.Dict:
    """
    Die Funktion move ist die Hauptlogik der Entscheidungsfindung der Schlange.

    Bewertet alle vier möglichen Bewegungsrichtungen ('up', 'down', 'left', 'right').
    Sie kombiniert dafür verschiedene Heuristiken (z. B. Futter, Freedom, Randabstand, Dead-Ends),
    und wählt die beste Option.

    Falls keine sichere oder sinnvolle Bewegung in eine der vier Richtungen gefunden wird, wird ein zufälliger, legaler Zug gewählt.

    Args:
        game_state (dict): Der aktuelle Spielzustand.

    Returns:
        dict: Der gewählte Zug in eine der Richtungen im Format {"move": "right"}.
    """
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
    """
    Startet den Battlesnake-Server
    """
    from server import run_server
    run_server({
        "info": info,
        "start": start,
        "move": move,
        "end": end,
    })
