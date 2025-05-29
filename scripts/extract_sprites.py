from PIL import Image
import os

# Loads sprite sheet
sheet = Image.open('assets/Snake.png').convert("RGBA")

# Uses assets for output folder
out_dir = 'assets/sprites'
os.makedirs(out_dir, exist_ok=True)

tile = 16
cols = sheet.width // tile
rows = sheet.height // tile

# Define your target colors
GREEN = (0, 255, 0)               # Snake segments
TAN   = (210, 180, 140)           # Recolored grass

for r in range(rows):
    for c in range(cols):
        # Crop one 16×16 tile
        box = (c*tile, r*tile, (c+1)*tile, (r+1)*tile)
        sprite = sheet.crop(box)

        pixels = sprite.load()
        # Decide what to do based on tile coords
        if (r, c) == (3, 2):
            # Rabbit: leave as-is
            pass
        elif (r, c) == (3, 3):
            # Grass: recolor to TAN
            for y in range(tile):
                for x in range(tile):
                    r0, g0, b0, a0 = pixels[x, y]
                    if a0:  # only modify non-transparent
                        pixels[x, y] = (TAN[0], TAN[1], TAN[2], a0)
        else:
            # Snake segments: recolor to GREEN
            for y in range(tile):
                for x in range(tile):
                    r0, g0, b0, a0 = pixels[x, y]
                    if a0:
                        pixels[x, y] = (GREEN[0], GREEN[1], GREEN[2], a0)

        # Save out as sprite_row_col.png
        sprite.save(f'{out_dir}/sprite_{r}_{c}.png')