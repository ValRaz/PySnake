import random
import arcade
from snake import Snake

# Sets up screen and grid cell sizes.
SCREEN_WIDTH  = 800
SCREEN_HEIGHT = 600
SCREEN_TITLE  = "PySnake"
GRID_SIZE     = 20
TOP_MARGIN    = 40

# Helper to convert grid coordinates to pixel positions on screen
def grid_pixel_conversion(position, grid_size):
    row, col = position
    x = col * grid_size + grid_size / 2
    y = TOP_MARGIN + row * grid_size + grid_size / 2
    return x, y

# Sets up window and background color
class GameWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.color.BLACK)

        # Text objects for Start screen, Score, Level, Level up, and Game Over
        self.start_title_text = arcade.Text(
            text="PySnake",
            x=SCREEN_WIDTH / 2,
            y=SCREEN_HEIGHT / 2 + 50,
            color=arcade.color.WHITE,
            font_size=54,
            anchor_x="center"
        )
        self.start_prompt_text = arcade.Text(
            text="Press S to Start",
            x=SCREEN_WIDTH / 2,
            y=SCREEN_HEIGHT / 2 - 10,
            color=arcade.color.LIGHT_GRAY,
            font_size=24,
            anchor_x="center"
        )

        self.score_text = arcade.Text(
            text="Score: 0",
            x=10,
            y=SCREEN_HEIGHT - 20,
            color=arcade.color.WHITE,
            font_size=20
        )
        self.level_text = arcade.Text(
            text="Level: 1",
            x=SCREEN_WIDTH - 80,
            y=SCREEN_HEIGHT - 20,
            color=arcade.color.WHITE,
            font_size=20
        )
        self.game_over_text = arcade.Text(
            text="GAME OVER",
            x=SCREEN_WIDTH / 2,
            y=SCREEN_HEIGHT / 2,
            color=arcade.color.RED,
            font_size=36,
            anchor_x="center"
        )
        self.restart_text = arcade.Text(
            text="Press R to Restart",
            x=SCREEN_WIDTH / 2,
            y=(SCREEN_HEIGHT / 2) - 40,
            color=arcade.color.WHITE,
            font_size=26,
            anchor_x="center"
        )

        self.level_banner_text = arcade.Text(
            text="",
            x=SCREEN_WIDTH / 2,
            y=SCREEN_HEIGHT / 2 + 20,
            color=arcade.color.YELLOW,
            font_size=32,
            anchor_x="center"
        )

        # Grass texture for empty cells
        self.grass_texture = arcade.load_texture("assets/sprites/sprite_3_3.png")

        # Sets game state
        self.game_state = "START"

        # Score / Level / Thresholds and level up banner duration
        self.score = 0
        self.level = 1
        self.next_level_threshold = 5
        self.level_increment = 10
        self.show_level_banner = False
        self.level_banner_timer = 0.0
        self.level_banner_duration = 1.0

        # Calculates grid dimensions and initializes snake at start position (middle)
        cols = SCREEN_WIDTH // GRID_SIZE
        rows = (SCREEN_HEIGHT - TOP_MARGIN) // GRID_SIZE - 3
        start_row = rows // 2
        start_col = cols // 2
        self.snake = Snake((start_row, start_col))
        self.segment_sprites = arcade.SpriteList()

        # Preload all snake segment textures
        self.textures = {}
        for idx in range(4):
            self.textures[("head", idx)] = arcade.load_texture(f"assets/sprites/sprite_0_{idx}.png")
        self.textures[("body_h", None)]   = arcade.load_texture("assets/sprites/sprite_1_0.png")
        self.textures[("body_v", None)]   = arcade.load_texture("assets/sprites/sprite_1_1.png")
        self.textures[("corner", (-1,0,0,1))]  = arcade.load_texture("assets/sprites/sprite_2_0.png")
        self.textures[("corner", (1,0,0,1))]   = arcade.load_texture("assets/sprites/sprite_2_1.png")
        self.textures[("corner", (1,0,0,-1))]  = arcade.load_texture("assets/sprites/sprite_2_2.png")
        self.textures[("corner", (-1,0,0,-1))] = arcade.load_texture("assets/sprites/sprite_2_3.png")
        self.textures[("tail_h", None)]  = arcade.load_texture("assets/sprites/sprite_3_0.png")
        self.textures[("tail_v", None)]  = arcade.load_texture("assets/sprites/sprite_3_1.png")

        # Initialize the food (rabbit sprite)
        self.food_sprite = arcade.Sprite(
            arcade.load_texture("assets/sprites/sprite_3_2.png"),
            scale=GRID_SIZE / 16
        )
        self.place_food()

        self.update_segment_sprites()

        # Movement speed timer
        self.time_since_move = 0.0
        self.move_interval = 0.15

        # Sound effects & Music
        self.eat_sound        = arcade.load_sound("assets/sounds/chomp_effect.mp3")
        self.background_music = arcade.load_sound("assets/sounds/background_music.mp3")
        self.level_up_sound   = arcade.load_sound("assets/sounds/level_up.mp3")
        self.level_player     = None
        self.music_player     = None

    # Spawn food at a random unoccupied whole cell
    def place_food(self):
        max_cols = SCREEN_WIDTH // GRID_SIZE
        max_rows = ((SCREEN_HEIGHT - TOP_MARGIN) // GRID_SIZE) - 3

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
            tex = self.textures[("head", 0)]
            sprite = arcade.Sprite(tex, scale=GRID_SIZE / tex.width)
            x, y = grid_pixel_conversion((r, c), GRID_SIZE)
            sprite.center_x = x
            sprite.center_y = y
            self.segment_sprites.append(sprite)
            return

        # Multi-segment load handling with corner segment preloading
        corner_map = {
            frozenset({(-1,0), (0,1)}):  self.textures[("corner", (-1,0,0,1))],
            frozenset({(1,0),  (0,1)}):  self.textures[("corner", (1,0,0,1))],
            frozenset({(1,0),  (0,-1)}): self.textures[("corner", (1,0,0,-1))],
            frozenset({(-1,0), (0,-1)}): self.textures[("corner", (-1,0,0,-1))],
        }

        for i, (r, c) in enumerate(segs):
            if i == 0:
                nr, nc = segs[1]
                dr, dc = r - nr, c - nc
                dir_map = {(0,1): 0, (1,0): 1, (0,-1): 2, (-1,0): 3}
                key = ("head", dir_map[(dr, dc)])
                tex = self.textures[key]
            elif i == length - 1:
                pr, pc = segs[-2]
                dr, dc = r - pr, c - pc
                if dr == 0:
                    tex = self.textures[("tail_h", None)]
                else:
                    tex = self.textures[("tail_v", None)]
            else:
                pr, pc = segs[i-1]
                nr, nc = segs[i+1]
                dr1, dc1 = r - pr, c - pc
                dr2, dc2 = nr - r, nc - c
                if dr1 == dr2 == 0:
                    tex = self.textures[("body_h", None)]
                elif dc1 == dc2 == 0:
                    tex = self.textures[("body_v", None)]
                else:
                    corner_key = frozenset({(dr1, dc1), (dr2, dc2)})
                    tex = corner_map.get(corner_key, self.textures[("body_h", None)])

            sprite = arcade.Sprite(tex, scale=GRID_SIZE / tex.width)
            x, y = grid_pixel_conversion((r, c), GRID_SIZE)
            sprite.center_x = x
            sprite.center_y = y
            self.segment_sprites.append(sprite)

    # Draws grid, food, and snake for each frame
    def on_draw(self):
        # Draws start screen
        if self.game_state == "START":
            self.clear()
            arcade.set_background_color(arcade.color.BLACK)
            self.start_title_text.draw()
            self.start_prompt_text.draw()
            return

        self.clear()
        rows = ((SCREEN_HEIGHT - TOP_MARGIN) // GRID_SIZE) - 3
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

        # Draws the food and then the snake on top
        arcade.draw_sprite(self.food_sprite)
        self.segment_sprites.draw()

        # Draws top divider line
        wall_y = SCREEN_HEIGHT - TOP_MARGIN
        arcade.draw_lrbt_rectangle_filled(
            left=0,
            right=SCREEN_WIDTH,
            top=wall_y,
            bottom=wall_y - 6,
            color=arcade.color.BLACK
        )

        # Updates and draws score and level
        self.score_text.text = f"Score: {self.score}"
        self.level_text.text = f"Level: {self.level}"
        self.score_text.draw()
        self.level_text.draw()

        # Draws level-up banner if needed
        if self.show_level_banner:
            self.level_banner_text.text = f"Level {self.level}"
            self.level_banner_text.draw()

        # Draws game over message
        if self.game_state == "GAME_OVER":
            self.game_over_text.draw()
            self.restart_text.draw()

    # Moves the snake and updates segment sprites
    def on_update(self, delta_time):
        if self.game_state != "PLAY":
            return

        # Movement timing
        self.time_since_move += delta_time
        if self.time_since_move < self.move_interval:
            return

        self.time_since_move = 0.0
        self.snake.move()

        # Grows snake and respawns eaten food
        if self.snake.segments[0] == self.food_position:
            self.snake.grow_flag = True
            self.place_food()
            self.score += 1
            arcade.play_sound(self.eat_sound)

        # Checks for wall collision
        head_row, head_col = self.snake.segments[0]
        cols = SCREEN_WIDTH // GRID_SIZE
        rows = (SCREEN_HEIGHT - TOP_MARGIN) // GRID_SIZE - 3

        if head_row < 0 or head_row >= rows or head_col < 0 or head_col >= cols:
            self.game_state = "GAME_OVER"
            if self.music_player:
                self.music_player.pause()
                self.music_player = None
            return

        # Checks for self-collision
        if self.snake.segments[0] in self.snake.segments[1:]:
            self.game_state = "GAME_OVER"
            if self.music_player:
                self.music_player.pause()
                self.music_player = None
            return

        # Check if score meets or exceeds the next level threshold, increase speed & show banner
        if (self.score >= self.next_level_threshold
            and not self.show_level_banner):
            self.level += 1
            self.move_interval = max(0.05, self.move_interval - 0.01)
            self.next_level_threshold += self.level_increment

            if self.music_player:
                self.music_player.pause()

            self.show_level_banner = True
            self.level_banner_timer = 0.0
            self.level_player = arcade.play_sound(self.level_up_sound)

        self.update_segment_sprites()

        # Manages banner timer
        if self.show_level_banner:
            self.level_banner_timer += delta_time
            if self.level_banner_timer >= self.level_banner_duration:
                self.show_level_banner = False

                # Stops level-up sound
                if self.level_player:
                    try:
                        self.level_player.stop()
                    except AttributeError:
                        pass
                    self.level_player = None

                # Restarts background music
                self.music_player = arcade.play_sound(self.background_music)

        if self.game_state == "GAME_OVER":
            if self.music_player:
                self.music_player.pause()
                self.music_player = None
            return

    # Resets grid and snake to start position
    def reset_game(self):
        cols = SCREEN_WIDTH // GRID_SIZE
        rows = (SCREEN_HEIGHT - TOP_MARGIN) // GRID_SIZE - 3
        start_row = rows // 2
        start_col = cols // 2

        # Re‐create a brand‐new single‐segment snake
        self.snake = Snake((start_row, start_col))
        self.segment_sprites = arcade.SpriteList()
        self.place_food()
        self.update_segment_sprites()

        self.time_since_move = 0.0
        self.move_interval = 0.15
        self.score = 0
        self.level = 1
        self.next_level_threshold = 5
        self.show_level_banner = False
        self.level_banner_timer = 0.0
        self.game_state = "PLAY"
        self.music_player = arcade.play_sound(self.background_music)

    # Handles start, reset, or arrow-key, and passes it to the grid and snake
    def on_key_press(self, key, modifiers):
        if self.game_state == "START" and key == arcade.key.S:
            self.game_state = "PLAY"
            self.music_player = arcade.play_sound(self.background_music)
            return

        if self.game_state == "GAME_OVER" and key == arcade.key.R:
            self.reset_game()
            return

        if self.game_state == "PLAY":
            self.snake.change_direction(key)

def main():
    window = GameWindow()
    arcade.run()

if __name__ == "__main__":
    main()