def move_position(position, move):
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

def off_board(board, pos):
    width = board["board"]["width"]
    height = board["board"]["height"]

    return pos["x"] < 0 or pos["x"] >= width or pos["y"] < 0 or pos["y"] >= height

class Battlesnake():
  # This generates a new baord from an initial board and a set of moves
  # This does NOT remove snakes that died, it just sets their health to 0
  # This means that the positions of the snakes MAY be off the board
  def generate_next_board(board, move_map):
    next_board = board.copy()

    for snake_id in move_map:
      move = move_map[snake_id]
      snake = [s for s in next_board["board"]["snakes"] if s["id"] == snake_id][0]

      # First we need to figure out where the new head should be
      next_position = move_position(snake["body"][0], move)

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
      if off_board(board, next_position):
        snake["health"] = 0

    # Now we check for collisions
    # One important thing to note, is that we do NOT mark death immediately
    # Instead we remember which snakes died, and makr them at the end
    # This is so there is no order depedency in the death marking and that
    # all body colillions are counted even if the snake you ran into also
    # collided with another snake. This means that if two snakes collide with
    # each others bodies, both will die.
    snake_collided = {}
    for snake_id in [s["id"] for s in next_board["board"]["snakes"] if s["health"] > 0]:
      snake_collided[snake_id] = False

    # First we will check for head to head collisions
    # If we find one, we will keep the longer snake alive.
    # If both snakes are the same length, they will both die.
    living_snake_ids = [s["id"] for s in next_board["board"]["snakes"] if s["health"] > 0]
    for snake_id in living_snake_ids:
      snake = [s for s in next_board["board"]["snakes"] if s["id"] == snake_id][0]

      collided_with = [s for s in next_board["board"]["snakes"] if s["id"] != snake_id and s["health"] > 0 and snake["head"] == s["head"]]
      if collided_with:
        # If the snakes are all the same length, they will all die
        if all([snake["length"] == s["length"] for s in collided_with]):
          snake_collided[snake_id] = True
        # Otherwise, we will keep the longer snake alive
        else:
          lengths = [s["length"] for s in collided_with]
          lengths.append(snake["length"])

          max_length = max(lengths)

          # If this snakes length is not the max, it dies
          if snake["length"] != max_length:
            snake_collided[snake_id] = True

    # Now we can check for body to body collisions
    for snake_id in living_snake_ids:
      snake = [s for s in next_board["board"]["snakes"] if s["id"] == snake_id][0]

      for other_snake_id in [s for s in living_snake_ids if s != snake_id]:
        other_snake = [s for s in next_board["board"]["snakes"] if s["id"] == other_snake_id][0]

        # We already checked for head to head collisions, so we can
        # only want to check the rest of the body here
        rest_of_other_body = other_snake["body"][1:]

        if snake["head"] in rest_of_other_body:
          snake_collided[snake_id] = True

    # Now that we've done all the collision detection, we can mark
    # the snakes that died
    for snake_id in snake_collided:
      if not snake_collided[snake_id]:
        continue
      snake = [s for s in next_board["board"]["snakes"] if s["id"] == snake_id][0]
      snake["health"] = 0

    # At the end here we need to update the `you` property
    # We do this by finding the correct snake in the new_board
    # and cloning it into the `you` property
    you = [s for s in next_board["board"]["snakes"] if s["id"] == next_board["you"]["id"]][0]
    next_board["you"] = you.copy()

    return next_board

