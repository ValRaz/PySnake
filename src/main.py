import random
import arcade
from src.snake import Snake

# Sets up screen and grid cell sizes.
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE = "PySnake"
GRID_SIZE = 20

#Helper to convert grid coordinates to pixel positions on screen
def grid_pixel_conversion(position, grid_size):
    row, col = position
    x = col * grid_size + grid_size / 2
    y = row * grid_size + grid_size / 2
    return x, y

# Sets up window and background color
class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)
        # Tan grass texture
        self.grass_texture = arcade.load_texture("assets/sprites/sprite_3_3.png")

        # Calculates grid dimensions and initializes snake at start position (middle)
        cols = SCREEN_WIDTH // GRID_SIZE
        rows = SCREEN_HEIGHT // GRID_SIZE
        start_row = rows // 2
        start_col = cols // 2
        self.snake = Snake((start_row, start_col))
        self.segment_sprites = arcade.SpriteList()

        # Preloads snake segment textures from assets
        self.textures = {}
        for idx in range(4):
            self.textures[('head', idx)] = arcade.load_texture(f"assets/sprites/sprite_0_{idx}.png")
        self.textures[('body_h', None)] = arcade.load_texture("assets/sprites/sprite_1_0.png")
        self.textures[('body_v', None)] = arcade.load_texture("assets/sprites/sprite_1_1.png")
        self.textures[('corner', (-1, 0, 0, 1))] = arcade.load_texture("assets/sprites/sprite_2_0.png")
        self.textures[('corner', (1, 0, 0, 1))]  = arcade.load_texture("assets/sprites/sprite_2_1.png")
        self.textures[('corner', (1, 0, 0, -1))] = arcade.load_texture("assets/sprites/sprite_2_2.png")
        self.textures[('corner', (-1, 0, 0, -1))]= arcade.load_texture("assets/sprites/sprite_2_3.png")
        self.textures[('tail_h', None)] = arcade.load_texture("assets/sprites/sprite_3_0.png")
        self.textures[('tail_v', None)] = arcade.load_texture("assets/sprites/sprite_3_1.png")

        # Initializes food with rabbit sprite
        self.food_sprite = arcade.Sprite(
            arcade.load_texture("assets/sprites/sprite_3_2.png"),
            scale=GRID_SIZE / 16
        )
        self.place_food()

        # Render the first load of the snake sprite
        self.update_segment_sprites()

        # Timer to control movement speed
        self.time_since_move = 0.0
        self.move_interval = 0.15

    # Spawn food at a random unoccupied grid cell
    def place_food(self):
        max_cols = SCREEN_WIDTH // GRID_SIZE
        max_rows = SCREEN_HEIGHT // GRID_SIZE
        while True:
            row = random.randrange(max_rows)
            col = random.randrange(max_cols)
            if (row, col) not in self.snake.segments:
                break
        self.food_position = (row, col)
        x, y = grid_pixel_conversion(self.food_position, GRID_SIZE)
        self.food_sprite.center_x = x
        self.food_sprite.center_y = y

    # Renders the snake sprites
    def update_segment_sprites(self):
        self.segment_sprites.clear()
        segs = self.snake.segments
        length = len(segs)

        # Single-segment first load
        if length == 1:
            r, c = segs[0]
            tex = self.textures[('head', 0)]
            sprite = arcade.Sprite(tex, scale=GRID_SIZE / tex.width)
            x, y = grid_pixel_conversion((r, c), GRID_SIZE)
            sprite.center_x = x
            sprite.center_y = y
            self.segment_sprites.append(sprite)
            return

        # Multi-segment load handling with corner segment preloading
        corner_map = {
            frozenset({(-1, 0), (0, 1)}): self.textures[('corner', (-1, 0, 0, 1))],
            frozenset({(1, 0),  (0, 1)}): self.textures[('corner', (1, 0, 0, 1))],
            frozenset({(1, 0),  (0, -1)}): self.textures[('corner', (1, 0, 0, -1))],
            frozenset({(-1, 0), (0, -1)}): self.textures[('corner', (-1, 0, 0, -1))]
        }

        for i, (r, c) in enumerate(segs):
            if i == 0:
                nr, nc = segs[1]
                dr, dc = r - nr, c - nc
                dir_map = {(0,1):0, (1,0):1, (0,-1):2, (-1,0):3}
                key = ('head', dir_map[(dr, dc)])
                tex = self.textures[key]
            elif i == length - 1:
                pr, pc = segs[-2]
                dr, dc = r - pr, c - pc
                key = ('tail_h', None) if dr == 0 else ('tail_v', None)
                tex = self.textures[key]
            else:
                pr, pc = segs[i-1]
                nr, nc = segs[i+1]
                dr1, dc1 = r - pr, c - pc
                dr2, dc2 = nr - r, nc - c

                if dr1 == dr2 == 0:
                    tex = self.textures[('body_h', None)]
                elif dc1 == dc2 == 0:
                    tex = self.textures[('body_v', None)]
                else:
                    corner_key = frozenset({(dr1, dc1), (dr2, dc2)})
                    tex = corner_map.get(corner_key, self.textures[('body_h', None)])

            sprite = arcade.Sprite(tex, scale=GRID_SIZE / tex.width)
            x, y = grid_pixel_conversion((r, c), GRID_SIZE)
            sprite.center_x = x
            sprite.center_y = y
            self.segment_sprites.append(sprite)

    # Draws grid, food, and snake for each frame
    def on_draw(self):
        self.clear()
        rows = SCREEN_HEIGHT // GRID_SIZE
        cols = SCREEN_WIDTH // GRID_SIZE

        # Draws grass for empty cells
        for row in range(rows):
            for col in range(cols):
                if (row, col) in self.snake.segments or (row, col) == self.food_position:
                    continue
                x, y = grid_pixel_conversion((row, col), GRID_SIZE)
                half = GRID_SIZE / 2
                rect = arcade.LBWH(x - half, y - half, GRID_SIZE, GRID_SIZE)
                arcade.draw_texture_rect(self.grass_texture, rect=rect)

        # Draws food and snake on top
        arcade.draw_sprite(self.food_sprite)
        self.segment_sprites.draw()

    # Moves the snake and updates segment sprites
    def on_update(self, delta_time):
        if self.snake.direction is None:
            return

        self.time_since_move += delta_time
        if self.time_since_move < self.move_interval:
            return

        self.time_since_move = 0.0
        self.snake.move()

        # Grows snake and respawns eaten food
        if self.snake.segments[0] == self.food_position:
            self.snake.grow_flag = True
            self.place_food()

        self.update_segment_sprites()

    # Handles arrow-key input and passes it to the snake
    def on_key_press(self, key, modifiers):
        self.snake.change_direction(key)

def main():
    window = GameWindow()
    arcade.run()

if __name__ == "__main__":
    main()