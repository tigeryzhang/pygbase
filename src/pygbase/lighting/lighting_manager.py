import pygame
import pygame._sdl2.video as sdl_video

from pygbase.common import Common

from ..camera import Camera
from .light import Light
from .shadow import Shadow


class LightingManager:
	def __init__(self, default_brightness: float, shadow_brightness: float):
		self.renderer: sdl_video.Renderer = Common.get("renderer")

		self.brightness = default_brightness
		self.shadow_brightness = shadow_brightness

		self.light_texture = sdl_video.Texture(self.renderer, Common.get("screen_size"), target=True)
		self.light_texture.blend_mode = pygame.BLENDMODE_MUL

		self.add_light_texture = sdl_video.Texture(self.renderer, Common.get("screen_size"), target=True)
		self.add_light_texture.blend_mode = pygame.BLENDMODE_ADD

		self.shadow_texture = sdl_video.Texture(self.renderer, Common.get("screen_size"), target=True)
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
		prev_target = self.renderer.target
		self.renderer.target = self.shadow_texture

		prev_draw_color = self.renderer.draw_color
		self.renderer.draw_color = (255,255,255)
		self.renderer.clear()
		self.renderer.draw_color = prev_draw_color

		# TODO: Make sure this actually works?
		Shadow.shadow_texture.alpha = int(self.shadow_brightness * 255)
		for shadow in self.shadows:
			shadow.draw(camera)

		self.renderer.target = prev_target

		self.shadow_texture.draw()

	def draw_lights(self, camera: Camera | None = None):
		prev_target = self.renderer.target
		prev_draw_color = self.renderer.draw_color

		# Multiplicative lighting
		self.renderer.target = self.light_texture
		brightness = int(self.brightness * 255)
		self.renderer.draw_color = (brightness, brightness, brightness)
		self.renderer.clear()

		for light in self.lights:
			light.draw_light(camera)

		# Add lighting
		self.renderer.target = self.add_light_texture
		self.renderer.draw_color = (0, 0, 0)
		self.renderer.clear()

		for light in self.lights:
			light.draw_add_light(camera)

		self.renderer.draw_color = prev_draw_color
		self.renderer.target = prev_target

		self.light_texture.draw()
		self.add_light_texture.draw()
