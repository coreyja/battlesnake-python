import unittest
import json

from battlesnake import Battlesnake

class TestStringMethods(unittest.TestCase):
    def load_json(self, filename):
      file = open(filename, 'r')
      return json.load(file)

    def test_no_collision(self):
      self.maxDiff = None

      original = self.load_json('fixtures/simple.json')
      expected = self.load_json('fixtures/simple_expected_no_collision.json')

      move_map = { 'Snake1':'left', 'Snake2':'right' }
      result = Battlesnake().generate_next_board(original, move_map)
      self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
