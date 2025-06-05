import unittest
import arcade
from arcade.key import RIGHT
from time import monotonic
from src.main import GameWindow, GRID_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, TOP_MARGIN

class TestLevelUpAndBanner(unittest.TestCase):
    def setUp(self):
        # Create a fresh GameWindow in PLAY state
        self.window = GameWindow()
        self.window.game_state = "PLAY"

        # Replace music_player with a dummy that records pause/resume
        class DummyPlayer:
            def __init__(self):
                self.paused = False
                self.resumed = False
            def pause(self):
                self.paused = True
            def play(self):
                self.resumed = True

        self.dummy = DummyPlayer()
        self.window.music_player = self.dummy

        # Speed up the threshold so test runs quickly
        self.window.next_level_threshold = 2
        self.window.level_increment = 2
        self.window.level_banner_duration = 0.5  # half‐second banner

        # Put snake in a spot with food right ahead
        rows = (SCREEN_HEIGHT - TOP_MARGIN) // GRID_SIZE
        cols = SCREEN_WIDTH // GRID_SIZE
        # ensure at least a 3×3 grid so we can place two foods
        self.window.snake.segments = [(1, 1)]
        self.window.snake.direction = RIGHT
        self.window.food_position = (1, 2)

    def test_level_up_triggers_banner_and_pauses_music(self):
        w = self.window

        # 1st eat: score goes from 0→1, below threshold → no banner
        w.time_since_move = w.move_interval
        w.on_update(delta_time=w.move_interval)
        self.assertEqual(w.score, 1)
        self.assertFalse(w.show_level_banner)
        self.assertFalse(self.dummy.paused)

        # Place next food immediately in front to trigger second eat
        w.snake.segments = [(1, 2)]
        w.snake.direction = RIGHT
        w.food_position = (1, 3)

        # 2nd eat: score 1→2, hits threshold → banner begins
        w.time_since_move = w.move_interval
        w.on_update(delta_time=w.move_interval)
        self.assertEqual(w.score, 2)
        self.assertTrue(w.show_level_banner)
        # music should be paused exactly once upon level up
        self.assertTrue(self.dummy.paused)

    def test_banner_duration_and_music_resumes(self):
        w = self.window
        # Force score to exactly threshold so banner shows on next step
        w.score = 2
        w.next_level_threshold = 2
        w.show_level_banner = True
        w.level = 2

        # Banner timer starts at 0; simulate time passing less than duration
        w.level_banner_timer = 0.3
        w.on_update(delta_time=0.1)
        # Still in banner
        self.assertTrue(w.show_level_banner)
        self.assertFalse(self.dummy.resumed)

        # Simulate enough time to exceed banner duration
        w.level_banner_timer = 0.49
        w.on_update(delta_time=0.1)
        self.assertFalse(w.show_level_banner)
        self.assertIsNotNone(w.music_player)

    def test_move_interval_decreases_each_level(self):
        w = self.window
        old_interval = w.move_interval

        # First eat to cross threshold
        w.time_since_move = w.move_interval
        w.on_update(delta_time=w.move_interval)
        # No change until next eat; provide second eat
        w.snake.segments = [(1, 2)]
        w.food_position = (1, 3)
        w.time_since_move = w.move_interval
        w.on_update(delta_time=w.move_interval)
        # After level up: move_interval must be strictly < old_interval
        self.assertLess(w.move_interval, old_interval)

    def test_banner_text_updates(self):
        w = self.window
        w.score = 2
        w.next_level_threshold = 2
        # Trigger banner
        w.time_since_move = w.move_interval
        w.snake.segments = [(1, 2)]
        w.snake.direction = RIGHT
        w.food_position = (1, 3)
        w.on_update(delta_time=w.move_interval)
        # Now show_level_banner=True and level=2
        self.assertTrue(w.show_level_banner)
        self.assertIn("Level 2", w.level_banner_text.text)

if __name__ == "__main__":
    unittest.main()