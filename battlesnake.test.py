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
    result = Battlesnake().generate_next_board(original, move_map)
    self.assertEqual(result, expected)

  def test_off_edge(self):
    original = self.load_json('fixtures/on_edge.json')
    expected = self.load_json('fixtures/on_edge_expected_off_board.json')

    move_map = { 'you':'left' }
    result = Battlesnake().generate_next_board(original, move_map)
    self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
