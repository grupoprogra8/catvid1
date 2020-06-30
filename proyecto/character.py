import arcade

from enum import IntEnum

class FACING(IntEnum):
    RIGHT_FACING = 0
    LEFT_FACING = 1

def load_texture_pair(filename):
    """
    Load a texture pair, with the second being a mirror image.
    """
    return [
        arcade.load_texture(filename),
        arcade.load_texture(filename, mirrored=True)
    ]

class PlayerCharacter(arcade.Sprite):
    """ Player Sprite"""
    def __init__(self, image_map, face_direction=FACING.RIGHT_FACING, scale=1.0):

        # Set up parent class
        super().__init__()

        # Default to face-right
        self.character_face_direction = face_direction

        # Used for flipping between image sequences
        self.cur_texture = 0
        self.scale = scale

        # Track our state
        self.jumping = False
        self.climbing = False
        self.is_on_ladder = False

        # --- Load Textures ---
        if type(image_map) is str:
            image_map = {
                "idle": image_map
            }

        # Load textures for idle standing
        if "idle" in image_map:
            self.idle_texture_pair = load_texture_pair(image_map["idle"])
        else:
            raise ValueError("idle image is mandatory")
        if "jump" in image_map:
            self.jump_texture_pair = load_texture_pair(image_map["jump"])
        else:
            self.jump_texture_pair = load_texture_pair(image_map["idle"])
        if "fall" in image_map:
            self.fall_texture_pair = load_texture_pair(image_map["fall"])
        else:
            self.fall_texture_pair = load_texture_pair(image_map["idle"])

        # Load textures for walking
        if "walk" in image_map:
            self.walk_textures = [load_texture_pair(img) for img in image_map["walk"]]
        else:
            self.walk_textures = [load_texture_pair(image_map["idle"])]

        # Load textures for climbing
        if "climbing" in image_map:
            self.climbing_textures = [load_texture_pair(img) for img in image_map["climbing"]]
        else:
            self.climbing_textures = [load_texture_pair(image_map["idle"])]

        # Set the initial texture
        self.texture = self.idle_texture_pair[0]

        # Hit box will be set based on the first image used. If you want to specify
        # a different hit box, you can do it like the code below.
        # self.set_hit_box([[-22, -64], [22, -64], [22, 28], [-22, 28]])
        self.set_hit_box(self.texture.hit_box_points)

    def update_animation(self, delta_time: float = 1/60):

        # Figure out if we need to flip face left or right
        if self.change_x < 0 and self.character_face_direction == FACING.RIGHT_FACING:
            self.character_face_direction = FACING.LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == FACING.LEFT_FACING:
            self.character_face_direction = FACING.RIGHT_FACING

        # Climbing animation
        if self.is_on_ladder:
            self.climbing = True
        if not self.is_on_ladder and self.climbing:
            self.climbing = False
        if self.climbing:
            if abs(self.change_y) > 1:
                self.cur_texture = (self.cur_texture + 1) % len(self.climbing_textures)
            else:
                self.cur_texture = 0
            self.texture = self.climbing_textures[self.cur_texture][self.character_face_direction]
            return

        # Jumping animation
        if self.change_y > 0 and not self.is_on_ladder:
            self.texture = self.jump_texture_pair[self.character_face_direction]
            return
        elif self.change_y < 0 and not self.is_on_ladder:
            self.texture = self.fall_texture_pair[self.character_face_direction]
            return

        # Idle animation
        if self.change_x == 0:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return

        # Walking animation
        self.cur_texture = (self.cur_texture + 1) % len(self.walk_textures)
        self.texture = self.walk_textures[self.cur_texture][self.character_face_direction]