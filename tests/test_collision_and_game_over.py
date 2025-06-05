import unittest
import arcade
from arcade.key import RIGHT, LEFT, UP, DOWN, R
from src.main import GameWindow, GRID_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT, TOP_MARGIN
from src.snake import Snake


class TestCollisionAndGameOver(unittest.TestCase):
    # Tests set up game window in Play state with dummy music player
    def setUp(self):
        self.window = GameWindow()
        self.window.game_state = "PLAY"
        class DummyPlayer:
            def __init__(self):
                self.paused = False
            def pause(self):
                self.paused = True

        self.window.music_player = DummyPlayer()

    # Tests top wall collision
    def test_wall_collision_top(self):

        max_rows = (SCREEN_HEIGHT - TOP_MARGIN) // GRID_SIZE - 3
        head_row = max_rows - 1
        head_col = 0
        self.window.snake.segments = [(head_row, head_col)]
        self.window.snake.direction = UP
        self.window.time_since_move = self.window.move_interval
        self.window.on_update(delta_time=self.window.move_interval)
        self.assertEqual(self.window.game_state, "GAME_OVER")
        self.assertTrue(self.window.music_player.paused)

    # Tests left, bottom and right wall collisions
    def test_walls_collision(self):
        w = self.window
        w.snake.direction = LEFT
        w.snake.segments = [(0, 0)]
        w.time_since_move = w.move_interval
        w.on_update(delta_time=w.move_interval)
        self.assertEqual(w.game_state, "GAME_OVER")

        # Resets and tests bottom collision
        self.setUp()
        max_rows = (SCREEN_HEIGHT - TOP_MARGIN) // GRID_SIZE - 3
        w = self.window
        w.snake.direction = DOWN
        w.snake.segments = [(0, 0)]
        w.time_since_move = w.move_interval
        w.on_update(delta_time=w.move_interval)
        self.assertEqual(w.game_state, "GAME_OVER")

        # Resets and tests right collision
        self.setUp()
        max_cols = SCREEN_WIDTH // GRID_SIZE - 3
        w = self.window
        w.snake.direction = RIGHT
        w.snake.segments = [(0, max_cols - 1)]
        w.time_since_move = w.move_interval
        w.on_update(delta_time=w.move_interval)
        self.assertEqual(w.game_state, "GAME_OVER")

    # Tests self collision
    def test_self_collision(self):
        w = self.window
        seq = [(2,2), (2,3), (3,3), (3,2), (2,2)]
        w.snake.segments = seq.copy()
        w.snake.direction = RIGHT
        w.time_since_move = w.move_interval
        w.on_update(delta_time=w.move_interval)
        self.assertEqual(w.game_state, "GAME_OVER")

    # Tests Reset
    def test_reset(self):
        w = self.window
        w.game_state = "GAME_OVER"
        w.score = 42
        w.level = 5
        w.move_interval = 0.02
        w.on_key_press(R, modifiers=0)
        self.assertEqual(w.game_state, "PLAY")
        self.assertEqual(w.score, 0)
        self.assertEqual(w.level, 1)
        self.assertAlmostEqual(w.move_interval, 0.15)

    # Tests no collision play
    def test_play_without_collisions(self):
        w = self.window
        rows = (SCREEN_HEIGHT - TOP_MARGIN) // GRID_SIZE - 3
        cols = SCREEN_WIDTH // GRID_SIZE
        center = (rows // 2, cols // 2)
        w.snake.segments = [center]
        w.snake.direction = RIGHT
        w.place_food()
        w.time_since_move = w.move_interval
        w.on_update(delta_time=w.move_interval)
        self.assertEqual(w.game_state, "PLAY")


if __name__ == "__main__":
    unittest.main()