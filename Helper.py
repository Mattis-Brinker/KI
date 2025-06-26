from collections import deque

def get_new_position(pos, move):
    """
   Bestimmt die neue Position, nach einer Bewegung.

    Args:
        pos (dict): Aktuelle Position als Dictionary mit Schlüsseln "x" und "y".
        move (str): Bewegungsrichtung ("up", "down", "left" oder "right").

    Returns:
        tuple: aktualisierte Koordinaten (x, y).
    """
  x, y = pos["x"], pos["y"]
  return {
      "up": (x, y + 1),
      "down": (x, y - 1),
      "left": (x - 1, y),
      "right": (x + 1, y),
  }[move]

def get_direction(start, end): 
    """
    Bestimmt die Bewegungsrichtung von einem Start- zu einem Endpunkt.

    Args:
        start (tuple): Ausgangskoordinaten (x, y).
        end (tuple): Zielkoordinaten (x, y).

    Returns:
        str: Bewegungsrichtung ("up", "down", "left" oder "right").
    """
  dx = end[0] - start[0]
  dy = end[1] - start[1]
  if dx == 1: return "right"
  if dx == -1: return "left"
  if dy == 1: return "up"
  if dy == -1: return "down"
  return "down"

def manhattan_dist(a, b):
    """
    Berechnet die Manhattan-Distanz zwischen zwei Punkten.

    Args:
        a (tuple): Koordinaten des Startpunktes (x, y).
        b (tuple): Koordinaten des Endpunktes (x, y).

    Returns:
        int: Abstand zwischen den zwei Punkten nach Manhatten-Metrik.
    """
  return abs(a[0] - b[0]) + abs(a[1] - b[1])

def is_safe(pos, game_state):
   """
    Überprüft, ob eine Position auf dem Spielfeld innerhalb der Spielfeldgrenzen liegt und ob sie durch eine gegnerische Schlange blockiert wird.

    Args:
        pos (tuple): Zu überprüfende Position (x, y).
        game_state (dict): Aktueller Spielzustand mit "board" und "you".

    Returns:
        bool: True, wenn die Position sicher ist, ansonsten False.
    """
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

def tailchase(new_pos, game_state):
   """
    Bewertet eine Bewegung basierend darauf, ob sie ihren eigenen Schwanz verfolgt.

    Args:
        new_pos (tuple): Neuer Positionspunkt (x, y) nach der Bewegung.
        game_state (dict): Aktueller Spielzustand mit "board" und "you".

    Returns:
        int: Prioritätswert (25 bei Erreichen des Schwanzes, ansonsten 0).
    """
  my_tail = game_state["you"]["body"][-1]
  if manhattan_dist(new_pos, (my_tail["x"], my_tail["y"])) == 0:
    return 25
  else:
    return 0

def freedom_score(pos, game_state):
   """
    Ermittelt die Bewegungsfreiheit ab einem gegebenen Punkt mit Breath-First-Search.

    Args:
        pos (tuple): Startpunkt (x, y) für die Flood-Fill-Erkundung.
        game_state (dict): Aktueller Spielzustand mit "board" und "you".

    Returns:
        int: Anzahl erreichbarer freier Felder (maximal 50).
    """
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
          if is_safe((nx, ny), game_state):
              queue.append((nx, ny))
  return count
