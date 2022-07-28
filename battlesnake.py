class Battlesnake():
  def generate_next_board(self, board, move_map):
    next_board = board.copy()

    for snake_id in move_map:
      move = move_map[snake_id]
      snake = [s for s in next_board["board"]["snakes"] if s["id"] == snake_id][0]

      # First we need to figure out where the new head should be
      next_position = self.move_position(snake["body"][0], move)

      # Then we can insert the new head
      snake["body"].insert(0, next_position)
      snake["head"] = next_position
      # And remove the old tail
      snake["body"].pop()

      # Reduce the snake health by 1
      new_health = snake["health"] - 1
      snake["health"] = new_health

      # If the new snake head is in the hazard sauce we need to
      # decrease the health equal to the hazard damage
      if any(next_position == h for h in board["board"]["hazards"]):
        new_health = snake["health"] - board["game"]["ruleset"]["settings"]["hazardDamagePerTurn"]
        snake["health"] = new_health

      # If the snake ate food, we set its health to 100
      # and we duplicate the tail, so that next turn the tail
      # doesn't change locations. We also make sure to update the length
      # property
      if any([next_position == f for f in board["board"]["food"]]):
        snake["health"] = 100
        tail = snake["body"][-1]
        snake["body"].append(tail)
        snake["length"] += 1

      # If the snake moved off the board we set its health to 0
      if self.off_board(board, next_position):
        snake["health"] = 0



    # At the end here we need to update the `you` property
    # We do this by finding the correct snake in the new_board
    # and cloning it into the `you` property
    you = [s for s in next_board["board"]["snakes"] if s["id"] == next_board["you"]["id"]][0]
    next_board["you"] = you.copy()

    return next_board

  def move_position(self, position, move):
    x = position["x"]
    y = position["y"]

    if move == "left":
      x -= 1
    elif move == "right":
      x += 1
    elif move == "up":
      y += 1
    elif move == "down":
      y -= 1
    else:
      raise Exception("Invalid move: " + move)

    return {"x": x, "y": y}

  def off_board(self, board, pos):
    width = board["board"]["width"]
    height = board["board"]["height"]

    return pos["x"] < 0 or pos["x"] >= width or pos["y"] < 0 or pos["y"] >= height
