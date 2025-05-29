from arcade.key import UP, DOWN, LEFT, RIGHT

class Snake:
   # Initializes a single segment snake at starting position
    def __init__(self, start_pos):
        self.segments = [start_pos]
        self.direction = None
        self.grow_flag = False

    # Changes snake direction per user input including ful 180 prevention
    def change_direction(self, key):
        if key == UP and self.direction != DOWN:
            self.direction = UP
        elif key == DOWN and self.direction != UP:
            self.direction = DOWN
        elif key == LEFT and self.direction != RIGHT:
            self.direction = LEFT
        elif key == RIGHT and self.direction != LEFT:
            self.direction = RIGHT

    # Moves snake forward if grow check is passed, removes tail if grow check is failed.
    def move(self):
        if self.direction is None:
            return

        head_r, head_c = self.segments[0]
        if self.direction == UP:
            head_r += 1
        elif self.direction == DOWN:
            head_r -= 1
        elif self.direction == LEFT:
            head_c -= 1
        elif self.direction == RIGHT:
            head_c += 1

        self.segments.insert(0, (head_r, head_c))

        if not self.grow_flag:
            self.segments.pop()
        else:
            self.grow_flag = False
