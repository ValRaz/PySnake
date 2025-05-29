import unittest
from src.snake import Snake
from arcade.key import RIGHT, LEFT, UP, DOWN

class TestSnake(unittest.TestCase):
    # Test move right goes from (5,5) to (5,6)
    def test_move_right(self):
        snake = Snake((5, 5))
        snake.direction = RIGHT
        snake.move()
        self.assertEqual(snake.segments[0], (5, 6))

    # Tests ignore 180 turn logic
    def test_prevent_reverse(self):
        snake = Snake((5, 5))
        snake.direction = RIGHT
        snake.change_direction(LEFT)
        snake.move()
        self.assertEqual(snake.segments[0], (5, 6))

    # Tests move left goes from (5,5) to (5,4)
    def test_move_left(self):
        snake = Snake((5, 5))
        snake.direction = LEFT
        snake.move()
        self.assertEqual(snake.segments[0], (5, 4))

    # Tests move up goes from (5,5) to (6,5)
    def test_move_up(self):
        snake = Snake((5, 5))
        snake.direction = UP
        snake.move()
        self.assertEqual(snake.segments[0], (6, 5))

    # Tests move down goes from (5,5) to (4,5)
    def test_move_down(self):
        snake = Snake((5, 5))
        snake.direction = DOWN
        snake.move()
        self.assertEqual(snake.segments[0], (4, 5))

    # Tests valid turn changes direction as expected
    def test_valid_turn(self):
        snake = Snake((5, 5))
        snake.direction = RIGHT
        snake.change_direction(UP)
        self.assertEqual(snake.direction, UP)

    # Test that move() does nothing when direction is None
    def test_no_move_when_direction_none(self):
        snake = Snake((5, 5))
        initial_segments = list(snake.segments)
        snake.move()
        self.assertEqual(snake.segments, initial_segments)

if __name__ == "__main__":
    unittest.main()