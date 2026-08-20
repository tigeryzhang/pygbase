import pygame

from pygbase.common import Common

from .. import Texture
from ..camera import Camera
from .light import Light
from .shadow import Shadow


class LightingManager:
	def __init__(self, default_brightness: float, shadow_brightness: float):
		self.renderer = Common.renderer

		self.brightness = default_brightness
		self.shadow_brightness = shadow_brightness

		self.light_texture = Texture(self.renderer, Common.get("screen_size"), target=True)
		self.light_texture.blend_mode = pygame.BLENDMODE_MUL

		self.add_light_texture = Texture(self.renderer, Common.get("screen_size"), target=True)
		self.add_light_texture.blend_mode = pygame.BLENDMODE_ADD

		self.shadow_texture = Texture(self.renderer, Common.get("screen_size"), target=True)
		self.shadow_texture.blend_mode = pygame.BLENDMODE_MUL

		self.lights: list[Light] = []
		self.shadows: list[Shadow] = []

	def add_light(self, light_source: Light) -> Light:
		self.lights.append(light_source)
		return light_source

	def remove_light(self, light_source: Light):
		if light_source in self.lights:
			self.lights.remove(light_source)

	def add_shadow(self, shadow: Shadow) -> Shadow:
		self.shadows.append(shadow)
		return shadow

	def remove_shadow(self, shadow: Shadow):
		if shadow in self.shadows:
			self.shadows.remove(shadow)

	def update(self, delta):
		# TODO: Don't actually need
		for light in self.lights:
			light.update(delta)

	def draw_shadows(self, camera: Camera | None = None):
		with self.renderer.using_target(self.shadow_texture):
			self.renderer.clear_with_color((255, 255, 255))

			Shadow.shadow_texture.alpha = int(self.shadow_brightness * 255)
			for shadow in self.shadows:
				shadow.draw(camera)

		self.shadow_texture.draw()

	def draw_lights(self, camera: Camera | None = None):
		# Multiplicative lighting
		with self.renderer.using_target(self.light_texture):
			brightness = int(self.brightness * 255)
			self.renderer.clear_with_color((brightness, brightness, brightness))

			for light in self.lights:
				light.draw_light(camera)

		# Add lighting
		with self.renderer.using_target(self.add_light_texture):
			self.renderer.clear_with_color((0, 0, 0))

			for light in self.lights:
				light.draw_add_light(camera)

		self.light_texture.draw()
		self.add_light_texture.draw()
