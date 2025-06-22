from Helper import is_safe, get_direction, freedom_score

def dead_end_bonus(move, new_pos, game_state):
  """Bewertet Moves, die in eine Sackgasse führen, aber den besten Ausweg wählen."""
  if not is_dead_end(new_pos, game_state):
      return 200

  longest_path = longest_path_in_area(new_pos, game_state)
  if longest_path and len(longest_path) > 1:
      expected_direction = get_direction(new_pos, longest_path[1])
      if expected_direction == move:
          return 100
  return 0

def is_dead_end(pos, game_state):
  """Eine Sackgasse liegt vor, wenn der frei erreichbare Raum eng und abgeschlossen ist."""
  freedom = freedom_score(pos, game_state)
  my_length = len(game_state["you"]["body"])
  if freedom < my_length+3:
      # wenig Raum: potenziell gefährlich
      return True
  return False

def longest_path_in_area(start, game_state):
  """Finde einen Pfad maximaler Länge im Bereich, den man von start aus erreichen kann."""
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