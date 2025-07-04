#Gruppe 19
#Teilnehmer:
#Rose, Lennnert 222201353
#Schlüter, Theo Peter 222201541
#Schubert, Philipp 220200128
#Brinker, Mattis Paul 222200558
from Helper import is_safe, get_direction, freedom_score

def dead_end_bonus(move, new_pos, game_state):
  """
    Bewertet einen Zug (Move), der in eine potenzielle Sackgasse führt.

    Falls die Position kein Dead-End (Sackgasse) ist, wird ein hoher Bonus (200) vergeben.
    Falls es eine Sackgasse ist, aber der Move in die Richtung des längsten verfügbaren Pfads zeigt, 
    gibt es einen kleineren Bonus (100).
    Andernfalls wird kein Bonus vergeben (0).

    Args:
        move (str): Die geplante Bewegungsrichtung ('up', 'down', 'left', 'right').
        new_pos (tuple): Die Position, die mit diesem Move erreicht wird (x, y).
        game_state (dict): Der aktuelle Spielzustand.

    Returns:
        int: Bonuswert für diesen Zug (0, 100 oder 200).
    """
  if not is_dead_end(new_pos, game_state):
      return 200

  longest_path = longest_path_in_area(new_pos, game_state)
  if longest_path and len(longest_path) > 1:
      expected_direction = get_direction(new_pos, longest_path[1])
      if expected_direction == move:
          return 100
  return 0

def is_dead_end(pos, game_state):
    """
    Bestimmt, ob eine gegebene Position als Sackgasse zählt, sprich ob der verfügbare Raum nicht ausreicht um überleben zu können.

    Eine Sackgasse liegt dann vor, wenn der verfügbare Raum kleiner als die eigene Schlangenlänge + 3 ist.

    Args:
        pos (tuple): Auf Sackgasse zu überprüfende Position (x, y).
        game_state (dict): Der aktuelle Spielzustand.

    Returns:
        bool: True, wenn die Position als Sackgasse eingestuft wird, sonst False.
    """
    freedom = freedom_score(pos, game_state)
    my_length = len(game_state["you"]["body"])
    if freedom < my_length+3:
      # wenig Raum: potenziell gefährlich
        return True
    return False

def longest_path_in_area(start, game_state):
  """
    Findet den längstmöglichen beschlängelbaren Pfad von einer gegebenen Startposition aus,
    unter Beachtung von Hindernissen (z. B. Schlangen, Wände), sprich es wird nur in "sichere" Felder gegangen. 
    Dafür wird eine Tiefensuche (DFS) verwendet.

    Args:
        start (tuple): Startposition (x, y).
        game_state (dict): Der aktuelle Spielzustand.

    Returns:
        list: Der längste gefundene Pfad als Liste von Positionen [(x1, y1), (x2, y2), ...].
    """
  visited = set()
  stack = [(start, [start])]
  longest_path = []

  while stack:
      current, path = stack.pop()
      if current in visited:
          continue
      visited.add(current)

      if len(path) > len(longest_path):
          longest_path = path

      for dx, dy in [(0,1),(0,-1),(1,0),(-1,0)]:
          neighbor = (current[0]+dx, current[1]+dy)
          if is_safe(neighbor, game_state) and neighbor not in path:
              stack.append((neighbor, path + [neighbor]))

  return longest_path
