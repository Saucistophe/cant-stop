import unittest
from unittest.mock import patch
from server import Game

class TestGetCombinations(unittest.TestCase):
    @patch.object(Game, 'load')
    def test_get_combinations_1234(self, mock_load):
        # Setup the game instance
        game = Game()
        
        game.players = ["Player 1"]
        game.current_player_idx = 0
        game.current_dice = [1, 2, 3, 4]
        game.allowed_dice_merge = 2
        
        # Execute the property under test
        result = game.get_combinations
        
        expected = [[3, 7], [4, 6], [5, 5]]
        
        # Check that we have the right combinations
        self.assertEqual(result, expected)

    @patch.object(Game, 'load')
    def test_get_combinations_1234_merge_1(self, mock_load):
        game = Game()
        game.players = ["Player 1"]
        game.current_dice = [1, 2, 3, 4]
        game.allowed_dice_merge = 1
        
        result = game.get_combinations
        expected = [[1, 2, 3, 4]]
        self.assertEqual(result, expected)

    @patch.object(Game, 'load')
    def test_get_combinations_1234_merge_4(self, mock_load):
        game = Game()
        game.players = ["Player 1"]
        game.current_dice = [1, 2, 3, 4]
        game.allowed_dice_merge = 4
        
        result = game.get_combinations
        expected = [[10]]
        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()
