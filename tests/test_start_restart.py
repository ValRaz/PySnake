import unittest
from arcade.key import S, R, RIGHT
from src.main import GameWindow

class TestStartAndRestart(unittest.TestCase):
    def setUp(self):
        self.window = GameWindow()
        # stub out music_player so on_key_press won’t error
        class Dummy:
            def __init__(self): pass
            def pause(self): pass
        self.window.music_player = Dummy()

    def test_start_key_transitions_to_play(self):
        w = self.window
        self.assertEqual(w.game_state, "START")
        # Pressing RIGHT before S: should stay in START
        w.on_key_press(RIGHT, modifiers=0)
        self.assertEqual(w.game_state, "START")

        # Pressing S transitions to PLAY and starts music_player
        w.on_key_press(S, modifiers=0)
        self.assertEqual(w.game_state, "PLAY")
        self.assertIsNotNone(w.music_player)

    def test_restart_key_only_in_game_over(self):
        w = self.window
        # Pressing R in START does nothing
        w.on_key_press(R, modifiers=0)
        self.assertEqual(w.game_state, "START")

        # Force game over, then R resets
        w.game_state = "GAME_OVER"
        w.score = 10
        w.level = 5
        w.move_interval = 0.03

        w.on_key_press(R, modifiers=0)
        # Should reset fields
        self.assertEqual(w.game_state, "PLAY")
        self.assertEqual(w.score, 0)
        self.assertEqual(w.level, 1)
        self.assertAlmostEqual(w.move_interval, 0.15)

    def test_arrow_keys_only_in_play(self):
        w = self.window
        # In START, arrow should not set snake.direction
        w.snake.direction = None
        w.on_key_press(RIGHT, modifiers=0)
        self.assertIsNone(w.snake.direction)

        # Move to PLAY
        w.on_key_press(S, modifiers=0)
        w.on_key_press(RIGHT, modifiers=0)
        self.assertEqual(w.snake.direction, RIGHT)

if __name__ == "__main__":
    unittest.main()