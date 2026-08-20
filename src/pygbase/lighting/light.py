import math

import pygame

from .. import Texture
from ..camera import Camera


class Light:
	light_texture: Texture

	def __init__(
		self,
		pos: pygame.typing.Point,
		brightness: float,
		radius: float,
		variation: float,
		variation_speed: float,
		camera_affected: bool = True,
		tint=(255, 255, 255),
	):
		self.start_time = pygame.time.get_ticks() / 1000

		self._linked_pos: bool
		if isinstance(pos, pygame.Vector2):
			self._linked_pos = True
			self.pos = pos
		else:
			self._linked_pos = False
			self.pos = pygame.Vector2(pos)

		self.brightness = pygame.math.clamp(brightness, 0, 1)
		self.add_brightness = pygame.math.clamp(brightness - 1, 0, 1)

		self.radius = radius
		self.variation = variation
		self.variation_speed = variation_speed

		self.tint = tint

		self.camera_affected = camera_affected

	def update_pos(self, pos):
		if self._linked_pos:
			raise RuntimeError("Cannot modify linked position")

		self.pos.update(pos)

	def set_brightness(self, brightness: float):
		self.brightness = pygame.math.clamp(brightness, 0, 1)
		self.add_brightness = pygame.math.clamp(brightness - 1, 0, 1)

	def update(self, delta):
		pass

	def draw_light(self, camera: Camera | None):
		current_time = pygame.time.get_ticks() / 1000
		variation = math.sin((current_time - self.start_time) * self.variation_speed) * self.variation

		size = int(self.radius + variation) * 2

		pos = self.pos
		if self.camera_affected and camera is not None:
			pos = camera.world_to_screen(pos)

		rect = pygame.Rect(0, 0, size, size)
		rect.center = pos

		Light.light_texture.alpha = int(self.brightness * 255)
		Light.light_texture.color = self.tint
		Light.light_texture.draw(dstrect=rect)

	def draw_add_light(self, camera: Camera | None):
		current_time = pygame.time.get_ticks() / 1000
		variation = math.sin((current_time - self.start_time) * self.variation_speed) * self.variation

		size = int(self.radius + variation) * 2

		pos = self.pos
		if self.camera_affected and camera is not None:
			pos = camera.world_to_screen(pos)

		rect = pygame.Rect(0, 0, size, size)
		rect.center = pos

		Light.light_texture.alpha = int(self.add_brightness * 255)
		Light.light_texture.color = self.tint
		Light.light_texture.draw(dstrect=rect)
