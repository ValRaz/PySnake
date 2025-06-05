import os
import sys
import unittest
from arcade.key import RIGHT
from src.main import GameWindow, GRID_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, TOP_MARGIN
from snake import Snake


class TestLevelUpAndBanner(unittest.TestCase):
    # Sets up game window for testing
    def setUp(self):
        self.window = GameWindow()
        self.window.game_state = "PLAY"
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
        self.window.next_level_threshold = 2
        self.window.level_increment = 2
        self.window.level_banner_duration = 0.5
        rows = (SCREEN_HEIGHT - TOP_MARGIN) // GRID_SIZE - 3
        cols = SCREEN_WIDTH // GRID_SIZE
        self.window.snake.segments = [(1, 1)]
        self.window.snake.direction = RIGHT
        self.window.food_position = (1, 2)

    # Tests level up banner trigger and music pausing
    def test_level_up_banner_and_pause_music(self):
        w = self.window
        w.time_since_move = w.move_interval
        w.on_update(delta_time=w.move_interval)
        self.assertEqual(w.score, 1)
        self.assertFalse(w.show_level_banner)
        self.assertFalse(self.dummy.paused)
        w.snake.segments = [(1, 2)]
        w.snake.direction = RIGHT
        w.food_position = (1, 3)

        w.time_since_move = w.move_interval
        w.on_update(delta_time=w.move_interval)
        self.assertEqual(w.score, 2)
        self.assertTrue(w.show_level_banner)
        self.assertTrue(self.dummy.paused)

    # Tests level banner display time and music restart
    def test_banner_duration_and_music_restart(self):
        w = self.window
        w.score = 2
        w.next_level_threshold = 2
        w.show_level_banner = True
        w.level = 2
        w.level_banner_timer = 0.3
        w.on_update(delta_time=0.1)
        self.assertTrue(w.show_level_banner)
        self.assertFalse(self.dummy.resumed)
        w.level_banner_timer = 0.49
        w.on_update(delta_time=0.1)
        self.assertFalse(w.show_level_banner)
        self.assertIsNotNone(w.music_player)

    # Tests move interval decreases per level
    def test_move_interval_decrease(self):
        w = self.window
        old_interval = w.move_interval
        w.time_since_move = w.move_interval
        w.on_update(delta_time=w.move_interval)
        w.snake.segments = [(1, 2)]
        w.food_position = (1, 3)
        w.time_since_move = w.move_interval
        w.on_update(delta_time=w.move_interval)
        self.assertLess(w.move_interval, old_interval)

    # Tests level banner text updates
    def test_banner_text_updates(self):
        w = self.window
        w.score = 2
        w.next_level_threshold = 2
        w.time_since_move = w.move_interval
        w.snake.segments = [(1, 2)]
        w.snake.direction = RIGHT
        w.food_position = (1, 3)
        w.on_update(delta_time=w.move_interval)
        w.on_draw()
        self.assertTrue(w.show_level_banner)
        self.assertIn("Level 2", w.level_banner_text.text)


if __name__ == "__main__":
    unittest.main()