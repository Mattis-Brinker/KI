# Gruppe 19
# Teilnehmer:
# Rose, Lennnert 222201353
# Schlüter, Theo Peter 222201541
# Schubert, Philipp 220200128
# Brinker, Mattis Paul 222200558

from collections import deque


def get_new_position(pos, move):
    """
    Bestimmt die neue Position nach einer Bewegung.

    Args:
        pos (dict): Aktuelle Position als Dictionary mit Schlüsseln "x" und "y".
        move (str): Bewegungsrichtung ("up", "down", "left" oder "right").

    Returns:
        tuple: Aktualisierte Koordinaten (x, y).
    """
    x, y = pos["x"], pos["y"]
    return {
        "up":    (x, y + 1),
        "down":  (x, y - 1),
        "left":  (x - 1, y),
        "right": (x + 1, y),
    }[move]


def get_direction(start, end):
    """
    Bestimmt die Bewegungsrichtung von einem Start- zu einem Endpunkt.

    Args:
        start (tuple): Ausgangskoordinaten (x, y).
        end   (tuple): Zielkoordinaten (x, y).

    Returns:
        str: Bewegungsrichtung ("up", "down", "left" oder "right").
    """
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    if dx == 1:
        return "right"
    if dx == -1:
        return "left"
    if dy == 1:
        return "up"
    if dy == -1:
        return "down"
    # Fallback – sollte eigentlich nie auftreten
    return "down"


def manhattan_dist(a, b):
    """
    Berechnet die Manhattan-Distanz zwischen zwei Punkten.

    Args:
        a (tuple): Koordinaten des Startpunktes (x, y).
        b (tuple): Koordinaten des Endpunktes (x, y).

    Returns:
        int: Abstand nach Manhattan-Metrik.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def is_safe(pos, game_state):
    """
    Prüft, ob eine Position frei und innerhalb des Spielfelds liegt.

    Args:
        pos (tuple): Zu prüfende Position (x, y).
        game_state (dict): Aktueller Spielzustand.

    Returns:
        bool: True, wenn sicher, sonst False.
    """
    x, y = pos
    # Spielfeldgrenzen
    if not (0 <= x < game_state["board"]["width"] and
            0 <= y < game_state["board"]["height"]):
        return False

    for snake in game_state["board"]["snakes"]:
        body = snake["body"]
        # Eigener Schwanz ist erst ab nächstem Zug blockiert
        segments = body[:-1] if snake["id"] == game_state["you"]["id"] else body
        for part in segments:
            if part["x"] == x and part["y"] == y:
                return False

    return True


def tailchase(new_pos, game_state):
    """
    Gibt Bonus-Punkte, wenn der Zug auf den eigenen Schwanz führt.

    Args:
        new_pos (tuple): Neue Position (x, y).
        game_state (dict): Aktueller Spielzustand.

    Returns:
        int: 25 bei Treffer, sonst 0.
    """
    my_tail = game_state["you"]["body"][-1]
    if manhattan_dist(new_pos, (my_tail["x"], my_tail["y"])) == 0:
        return 25
    return 0


def freedom_score(pos, game_state, limit=50):
    """
    Flood-Fill (BFS), um die freie Fläche ab einer Position zu zählen.

    Args:
        pos (tuple): Startpunkt (x, y).
        game_state (dict): Aktueller Spielzustand.
        limit (int): Maximale Felder (Laufzeitbeschränkung).

    Returns:
        int: Anzahl erreichbarer Felder (≤ limit).
    """
    visited = set()
    queue = deque([pos])
    count = 0

    while queue and count < limit:
        x, y = queue.popleft()
        if (x, y) in visited:
            continue
        visited.add((x, y))
        count += 1

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if (nx, ny) not in visited and is_safe((nx, ny), game_state):
                queue.append((nx, ny))

    return count
