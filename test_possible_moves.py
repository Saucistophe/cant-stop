import pytest
from server import Game, Player

def test_possible_moves_filters_captured_rows():
    game = Game()
    # Player 0 has captured row 7 (hook value 6 equals row 7 length 6)
    p0 = Player(name="p0", hooks={7: 6})
    p1 = Player(name="p1", markers={})
    game.players = [p0, p1]
    game.rows = {7: 6}
    game.current_player_idx = 1 # p1's turn
    game.current_dice = [3, 4, 3, 4]
    game.allowed_dice_merge = 2
    game.max_markers = 3

    # game.combinations() should return [[7, 7]]
    # Since row 7 is captured, [7, 7] should be filtered out.

    moves = game.possible_moves
    assert [7, 7] not in moves, f"Expected [7, 7] to be filtered out, but got {moves}"

def test_possible_moves_returns_candidate_moves():
    game = Game()
    p0 = Player(name="p0", markers={2: 1, 3: 1, 4: 1}) # Already has 3 markers
    game.players = [p0]
    game.current_player_idx = 0
    game.max_markers = 3
    game.current_dice = [5, 6, 5, 6] # sum is 11, 11
    game.allowed_dice_merge = 2
    game.rows = {11: 10}

    # p0 has 3 markers (2, 3, 4). Move [11, 11] requires a new marker.
    # So 11 should be skipped. candidate_move becomes empty.
    # possible_moves should return []

    moves = game.possible_moves
    assert moves == [], f"Expected no possible moves due to max markers, but got {moves}"
