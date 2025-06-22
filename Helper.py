from collections import deque

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

def manhattan_dist(a, b):
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

def tailchase(new_pos, game_state):
  my_tail = game_state["you"]["body"][-1]
  if manhattan_dist(new_pos, (my_tail["x"], my_tail["y"])) == 0:
    return 25
  else:
    return 0

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
          if is_safe((nx, ny), game_state):
              queue.append((nx, ny))
  return count