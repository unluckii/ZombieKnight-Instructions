import pygame

from settings import WINDOW_WIDTH, WINDOW_HEIGHT


RUBY_FRAMES = [f"tile00{i}.png" for i in range(7)]


def load_frames(folder, filenames, size):
    """Load and scale a list of sprite frames from a folder."""
    return [
        pygame.transform.scale(pygame.image.load(f"{folder}/{name}"), size)
        for name in filenames
    ]


def flip_frames(frames):
    """Return a list of horizontally-flipped copies of the given frames."""
    return [pygame.transform.flip(s, True, False) for s in frames]


def advance_frame(current, sprite_list, speed):
    """Advance an animation index, wrapping at the end.
    Returns (new_index, wrapped_bool) — wrapped is True the frame the cycle resets."""
    if current < len(sprite_list) - 1:
        return current + speed, False
    return 0, True


def teleport(sprite):
    """Move a sprite to the opposite portal exit and update its rect."""
    if sprite.position.x > WINDOW_WIDTH // 2:
        sprite.position.x = 86
    else:
        sprite.position.x = WINDOW_WIDTH - 150

    if sprite.position.y > WINDOW_HEIGHT // 2:
        sprite.position.y = 64
    else:
        sprite.position.y = WINDOW_HEIGHT - 132

    sprite.rect.bottomleft = sprite.position


def handle_portal_collision(sprite):
    """If sprite hit a portal, play its sound and teleport.
    Requires sprite to have .portal_group, .portal_sound, .position, .rect."""
    if pygame.sprite.spritecollide(sprite, sprite.portal_group, False):
        sprite.portal_sound.play()
        teleport(sprite)

def apply_motion(sprite):
    """Integrate kinematics, wrap horizontally, sync rect to position.
    Requires sprite to have .velocity, .acceleration, .position, .rect."""
    sprite.velocity += sprite.acceleration
    sprite.position += sprite.velocity + 0.5 * sprite.acceleration

    if sprite.position.x < 0:
        sprite.position.x = WINDOW_WIDTH
    elif sprite.position.x > WINDOW_WIDTH:
        sprite.position.x = 0

    sprite.rect.bottomleft = sprite.position