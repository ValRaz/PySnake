import unittest
from arcade.key import RIGHT
from src.snake import Snake
from src.main import GameWindow, GRID_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

class TestGrowthAndFood(unittest.TestCase):
    # Tests snake growth logic
    def test_snake_grows_when_flagged(self):
        snake = Snake((0, 0))
        initial_length = len(snake.segments)
        snake.grow_flag = True
        snake.direction = RIGHT
        snake.move()
        self.assertEqual(len(snake.segments), initial_length + 1)

    #Tests food placement, not on occupied cell or taking more than one cell
    def test_place_food_not_on_snake(self):
        window = GameWindow()
        max_cols = SCREEN_WIDTH // GRID_SIZE
        max_rows = SCREEN_HEIGHT // GRID_SIZE
        occupied = [(r, c) for r in range(max_rows) for c in range(max_cols - 1)]
        window.snake.segments = occupied.copy()
        window.place_food()
        self.assertNotIn(window.food_position, occupied)
        r, c = window.food_position
        self.assertTrue(0 <= r < max_rows)
        self.assertTrue(0 <= c < max_cols)

if __name__ == "__main__":
    unittest.main()