import pygame
import pygame._sdl2.video as sdl_video

from ..common import Common
from .light import Light
from .lighting_manager import LightingManager
from .shadow import Shadow

__all__ = ["Light", "LightingManager", "Shadow"]


# TODO: Honestly the entire lighting system should probably be redesigned one day
def init_lighting_system():
	generate_lights(256)
	generate_shadows(256)


def generate_lights(radius: int, power: float = 1.4):
	resolution = radius * 2

	light_texture = sdl_video.Texture(
		Common.get("renderer"),
		(
			resolution,
			resolution,
		),
	)
	light_texture.blend_mode = pygame.BLENDMODE_ADD

	light_surf = pygame.Surface((resolution, resolution), flags=pygame.SRCALPHA)
	for inner in range(radius, 0, -1):
		factor = 1 - (inner / radius) ** power
		colour = int(255 * factor)

		pygame.draw.circle(
			light_surf,
			(colour, colour, colour, colour),
			(radius, radius),
			inner,
		)

	light_texture.update(light_surf)
	Light.light_texture = light_texture


def generate_shadows(radius: int, power: float = 3):
	resolution = radius * 2

	shadow_texture = sdl_video.Texture(
		Common.get("renderer"),
		(
			resolution,
			resolution,
		),
	)
	shadow_texture.blend_mode = pygame.BLENDMODE_ADD

	# Create the largest shadow surface
	shadow_surf = pygame.Surface((resolution, resolution), flags=pygame.SRCALPHA)
	for inner in range(radius, 0, -1):
		factor = 1 - (inner / radius) ** power
		colour = int(255 * factor)

		pygame.draw.circle(
			shadow_surf,
			(colour, colour, colour, colour),
			(radius, radius),
			inner,
		)

	shadow_texture.update(shadow_surf)
	Shadow.shadow_texture = shadow_texture
