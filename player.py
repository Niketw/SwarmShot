import pygame
import math

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 2  # Movement speed

        # Load the sprite sheet
        self.sprite_sheet = pygame.image.load("Sprites/Sprites_Player/mega_scientist_walk.png").convert_alpha()
        self.current_frame = 0
        self.frame_timer = 0
        self.frame_delay = 10  # Adjusts animation speed

        # Player direction and frame setup
        self.direction = "down"  # Default direction
        self.frames = self.load_frames()

    def load_frames(self):
        """Extract frames from sprite sheet for animation."""
        frames = {
            "up": [self.sprite_sheet.subsurface((i * 64, 0, 64, 64)) for i in range(8)],
            "left": [self.sprite_sheet.subsurface((i * 64, 64, 64, 64)) for i in range(8)],
            "down": [self.sprite_sheet.subsurface((i * 64, 128, 64, 64)) for i in range(8)],
            "right": [self.sprite_sheet.subsurface((i * 64, 192, 64, 64)) for i in range(8)],
        }
        return frames

    def update(self, keys):
        """Update player position and animation based on input."""
        moving = False
        move_x, move_y = 0, 0

        # Check vertical movement (up/down)
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            move_y -= 1
            self.direction = "up"
            moving = True
        elif keys[pygame.K_DOWN] or keys[pygame.K_s]:
            move_y += 1
            self.direction = "down"
            moving = True

        # Check horizontal movement (left/right)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            move_x -= 1
            self.direction = "left"
            moving = True
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            move_x += 1
            self.direction = "right"
            moving = True

        # Normalize diagonal movement to ensure consistent speed
        if move_x != 0 and move_y != 0:
            # If moving diagonally, normalize the vector to prevent faster diagonal movement
            length = math.sqrt(move_x ** 2 + move_y ** 2)
            move_x /= length
            move_y /= length

        # Apply the movement
        self.x += move_x * self.speed
        self.y += move_y * self.speed

        # Update animation frame
        if moving:
            self.frame_timer += 1
            if self.frame_timer >= self.frame_delay:
                self.frame_timer = 0
                self.current_frame = (self.current_frame + 1) % len(self.frames[self.direction])
        else:
            self.current_frame = 0  # Idle state resets to the first frame

    def draw(self, surface):
        """Draw the player sprite on the screen."""
        surface.blit(self.frames[self.direction][self.current_frame], (self.x, self.y))
