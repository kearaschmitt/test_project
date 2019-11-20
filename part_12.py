"""
Lab 12 Arcade Game
"""
import arcade

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650

# Sprite Scaling
CHARACTER_SCALING = 0.25
TILE_SCALING = 0.25
TILE_SIZE = 128
SCALED_TILE_SIZE = (TILE_SIZE * TILE_SCALING)

# Movement Speed (pixels per frame)
PLAYER_MOVEMENT_SPEED = 10
GRAVITY = 1
PLAYER_JUMP_SPEED = 15

# Character/Screen Margins
VIEWPORT_MARGIN = 100
RIGHT_MARGIN = 150


class MyWindow(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT)

        # Sprite lists
        self.player_list = None
        self.wall_list = None
        self.star_list = None
        self.obstacles_list = None

        # Set up the player
        self.player_sprite = None

        # Physics engine
        self.physics_engine = None

        # Used for scrolling map
        self.view_left = 0
        self.view_bottom = 0

        self.score = 0

    def setup(self):

        # Sprite lists
        self.player_list = arcade.SpriteList()
        self.wall_list = arcade.SpriteList()
        self.star_list = arcade.SpriteList()
        self.obstacles_list = arcade.SpriteList()

        # Set up the player
        self.player_sprite = arcade.Sprite("alienBlue_front.png", CHARACTER_SCALING)

        # Starting position of the player
        self.player_sprite.center_x = 60
        self.player_sprite.center_y = 170
        self.player_list.append(self.player_sprite)

        # --- load in the map from the tiled editor ---
        map_name = ".../Lab 12 - Final Lab/lab_12_map.tmx"

        my_map = arcade.tilemap.read_tmx("lab_12_map.tmx")

        # -- Platforms
        self.wall_list = arcade.tilemap.process_layer(my_map, "Tile Layer 1", TILE_SCALING)

        # -- Stars
        self.star_list = arcade.tilemap.process_layer(my_map, "Tile Layer 2", TILE_SCALING)

        # -- Obstacles
        self.obstacles_list = arcade.tilemap.process_layer(my_map, "Tile Layer 3", TILE_SCALING)

        # Create out platformer physics engine with gravity
        self.physics_engine = arcade.PhysicsEnginePlatformer(self.player_sprite, self.wall_list, GRAVITY)

        # Set the background color
        arcade.set_background_color(arcade.color.PALATINATE_PURPLE)

        # Set the view port boundaries
        # These numbers set where we have 'scrolled' to.
        self.view_left = 0
        self.view_bottom = 0

        self.score = 0

    def on_draw(self):
        arcade.start_render()

        # Draw all the sprites.
        self.wall_list.draw()
        self.player_list.draw()
        self.star_list.draw()

        # record score on screen
        arcade.draw_text(f"Score: {self.score}", 16 + self.view_left, 8 + self.view_bottom,
                         arcade.color.BLACK, 16)

        obstacle_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.obstacles_list)
        if obstacle_hit_list:
            arcade.draw_text("Game Over!", 325, 300, arcade.color.WHITE, 26)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0

    def update(self, delta_time):

        self.physics_engine.update()

        star_hit_list = arcade.check_for_collision_with_list(self.player_sprite,
                                                             self.star_list)

        for star in star_hit_list:
            star.remove_from_sprite_lists()
            # arcade.play_sound(self.collect_coin_sound)
            self.score += 1

        # --- Manage Scrolling ---
        # Track if we need to change the view port

        changed = False

        # Scroll left
        left_boundary = self.view_left + VIEWPORT_MARGIN
        if self.player_sprite.left < left_boundary:
            self.view_left -= left_boundary - self.player_sprite.left
            changed = True

        # Scroll right
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_MARGIN
        if self.player_sprite.right > right_boundary:
            self.view_left += self.player_sprite.right - right_boundary
            changed = True

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - VIEWPORT_MARGIN
        if self.player_sprite.top > top_boundary:
            self.view_bottom += self.player_sprite.top - top_boundary
            changed = True

        # Scroll down
        bottom_boundary = self.view_bottom + VIEWPORT_MARGIN
        if self.player_sprite.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player_sprite.bottom
            changed = True

        # If we need to scroll, go ahead and do it.
        if changed:
            arcade.set_viewport(self.view_left,
                                SCREEN_WIDTH + self.view_left,
                                self.view_bottom,
                                SCREEN_HEIGHT + self.view_bottom)


def main():
    window = MyWindow()
    window.setup()

    arcade.run()


main()