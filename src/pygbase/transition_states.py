import pygame

from . import Texture
from .common import Common
from .scene import Scene


class Transition(Scene, name="_transition"):
	def __init__(self, current_state: Scene, to_state: Scene):
		super().__init__(clear_color=None)

		self.current_state = current_state
		self.to_state = to_state

	def update(self, delta: float):
		pass


class FadeTransition(Transition, name="fade_transition"):
	def __init__(
		self,
		current_state: Scene,
		to_state: Scene,
		transition_time: float,
		fade_colour: tuple[int, int, int],
	):
		super().__init__(current_state, to_state)

		self.transition_time = transition_time

		self.fade_colour = fade_colour

		self.fade_amount = 0
		self.fade_in = True

		fade_surface = pygame.Surface(
			(Common.get("screen_width"), Common.get("screen_height")),
			flags=pygame.SRCALPHA,
		)
		fade_surface.fill(self.fade_colour)
		self.fade_texture = Texture.from_surface(
			Common.renderer,
			fade_surface,
		)

	def update(self, delta: float):
		self.fade_texture.alpha = self.fade_amount

		if self.fade_in:
			self.fade_amount += 255 / (self.transition_time / 2) * delta
			if self.fade_amount >= 255:
				self.fade_amount = 255
				self.fade_in = False

			self.current_state.update(delta)
		else:
			self.fade_amount -= 255 / (self.transition_time / 2) * delta
			if self.fade_amount <= 0:
				self.set_next_state(self.to_state)

			self.to_state.update(delta)

	def draw(self):
		if self.fade_in:
			self.current_state.draw()
		else:
			self.to_state.draw()

		self.fade_texture.draw()
