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
    
    # Combinations are [[6, 8], [7, 7]]
    # Since row 7 is captured, [7, 7] should be filtered out.
    # [6, 8] should remain because 6 and 8 are not captured (not even in rows)
    
    moves = game.possible_moves
    
    print(f"Test 1 - moves: {moves}")
    assert [7, 7] not in moves, f"Expected [7, 7] to be filtered out, but got {moves}"
    assert [6, 8] in moves, f"Expected [6, 8] to be present, but got {moves}"

def test_possible_moves_returns_candidate_moves():
    game = Game()
    p0 = Player(name="p0", markers={2: 1, 3: 1, 4: 1}) # Already has 3 markers
    game.players = [p0]
    game.current_player_idx = 0
    game.max_markers = 3
    game.current_dice = [5, 6, 5, 6] # combinations [[10, 12], [11, 11]]
    game.allowed_dice_merge = 2
    game.rows = {10: 5, 11: 5, 12: 5}
    
    # p0 has 3 markers (2, 3, 4). 
    # Move [10, 12] requires 2 new markers (10 and 12).
    # Move [11, 11] requires 1 new marker (11).
    # Since max_markers is 3 and p0 already has 3, no NEW markers can be added.
    # So both moves should be filtered out.
    
    moves = game.possible_moves
    print(f"Test 2 - moves: {moves}")
    assert moves == [], f"Expected no possible moves due to max markers, but got {moves}"

if __name__ == "__main__":
    try:
        test_possible_moves_filters_captured_rows()
        print("Test 1 passed")
    except AssertionError as e:
        print(f"Test 1 failed: {e}")
    except Exception as e:
        print(f"Test 1 error: {e}")

    try:
        test_possible_moves_returns_candidate_moves()
        print("Test 2 passed")
    except AssertionError as e:
        print(f"Test 2 failed: {e}")
    except Exception as e:
        print(f"Test 2 error: {e}")
