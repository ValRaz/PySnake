import unittest
from arcade.key import S, R, RIGHT
from src.main import GameWindow

class TestStartAndRestart(unittest.TestCase):
    # Sets up game window for testing
    def setUp(self):
        self.window = GameWindow()
        class Dummy:
            def __init__(self): pass
            def pause(self): pass
        self.window.music_player = Dummy()

    # Tests that start key changes game state to play
    def test_start(self):
        w = self.window
        self.assertEqual(w.game_state, "START")
        w.on_key_press(RIGHT, modifiers=0)
        self.assertEqual(w.game_state, "START")
        w.on_key_press(S, modifiers=0)
        self.assertEqual(w.game_state, "PLAY")
        self.assertIsNotNone(w.music_player)

    # Tests restart key works only in game over 
    def test_restart(self):
        w = self.window
        w.on_key_press(R, modifiers=0)
        self.assertEqual(w.game_state, "START")
        w.game_state = "GAME_OVER"
        w.score = 10
        w.level = 5
        w.move_interval = 0.03
        w.on_key_press(R, modifiers=0)
        self.assertEqual(w.game_state, "PLAY")
        self.assertEqual(w.score, 0)
        self.assertEqual(w.level, 1)
        self.assertAlmostEqual(w.move_interval, 0.15)

    # Tests arrow keys work only during play
    def test_arrow_keys(self):
        w = self.window
        w.snake.direction = None
        w.on_key_press(RIGHT, modifiers=0)
        self.assertIsNone(w.snake.direction)
        w.on_key_press(S, modifiers=0)
        w.on_key_press(RIGHT, modifiers=0)
        self.assertEqual(w.snake.direction, RIGHT)

if __name__ == "__main__":
    unittest.main()