import unittest
import json

from battlesnake import Battlesnake

class TestStringMethods(unittest.TestCase):
  def __init__(self, *args, **kwargs):
    super(TestStringMethods, self).__init__(*args, **kwargs)
    self.maxDiff = None

  def load_json(self, filename):
    file = open(filename, 'r')
    loaded = json.load(file)
    file.close()
    return loaded

  def test_no_collision(self):
    original = self.load_json('fixtures/simple.json')
    expected = self.load_json('fixtures/simple_expected_no_collision.json')

    move_map = { 'Snake1':'left', 'Snake2':'right' }
    result = Battlesnake.generate_next_board(original, move_map)
    self.assertEqual(result, expected)

  def test_off_edge(self):
    original = self.load_json('fixtures/on_edge.json')
    expected = self.load_json('fixtures/on_edge_expected_off_board.json')

    move_map = { 'you':'left' }
    result = Battlesnake.generate_next_board(original, move_map)
    self.assertEqual(result, expected)

  def test_ate_food(self):
    original = self.load_json('fixtures/on_edge.json')
    expected = self.load_json('fixtures/on_edge_expected_ate_food.json')

    move_map = { 'you':'right' }
    result = Battlesnake.generate_next_board(original, move_map)
    self.assertEqual(result, expected)

  def test_single_hazard(self):
    original = self.load_json('fixtures/simple.json')
    expected = self.load_json('fixtures/simple_expected_single_hazard.json')

    move_map = { 'Snake1':'down', 'Snake2':'up' }
    result = Battlesnake.generate_next_board(original, move_map)
    self.assertEqual(result, expected)

  def test_head_to_head(self):
    original = self.load_json('fixtures/simple.json')
    expected = self.load_json('fixtures/simple_expected_head_to_head.json')

    move_map = { 'Snake1':'down', 'Snake2':'left' }
    result = Battlesnake.generate_next_board(original, move_map)
    self.assertEqual(result, expected)

  def test_double_body_collision(self):
    original = self.load_json('fixtures/double_body_collision.json')
    expected = self.load_json('fixtures/double_body_collision_expected.json')

    move_map = { 'you':'right', 'Snake1':'left' }
    result = Battlesnake.generate_next_board(original, move_map)
    self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
