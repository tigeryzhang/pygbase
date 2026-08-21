import gc
import logging
from collections.abc import Callable

import pygame

import pygbase

from .common import Common
from .debug import Debug
from .events import Events
from .inputs.input import Input
from .loader import Loading
from .renderer import Renderer
from .scene import Scene

logger = logging.getLogger(__name__)


class App:
	def __init__(
		self,
		after_load_state: type[Scene],
		title: str = "Pygbase Window",
		fixed_time_fps: int = 60,
		vsync: bool = True,
		run_on_load_complete: tuple[Callable, ...] = (),
	):
		self.is_running: bool = True

		self.title = title

		self.window = pygame.Window(title, Common.get("screen_size"))
		self.renderer = Renderer(self.window, vsync=vsync, target_texture=True)
		Common.renderer = self.renderer

		Debug.init()

		self.clock: pygame.time.Clock = pygame.time.Clock()

		load_complete_runners = (pygbase.lighting.init_lighting_system,) + run_on_load_complete
		self.scene: Loading | Scene = Loading(after_load_state, load_complete_runners)

		self.fixed_time_rate = 1 / fixed_time_fps

		Events.add_handler("all", pygame.QUIT, self.quit_handler)

	def quit_handler(self, _event: pygame.event.Event):
		self.is_running = False

	def handle_events(self):
		Input.reset()
		Events.handle_events(self.scene.id)

	def update(self, delta):
		self.scene.update(delta)

	def fixed_update(self):
		self.scene.fixed_update(self.fixed_time_rate)

	def draw(self):
		if self.scene.clear_color is not None:
			self.renderer.clear_with_color(self.scene.clear_color)
		self.scene.draw()

	def switch_state(self):
		next_state = self.scene.get_next_state()
		if self.scene is not next_state:
			self.scene.exit()

			self.scene = self.scene.get_next_state()
			self.scene.enter()

			logger.debug("Switching scene, running garbage collector...")
			gc.collect()

	def run(self):
		self.is_running = True

		update_timer = 0.0

		while self.is_running:
			# Timing
			delta = min(self.clock.tick() / 1000, 0.12)
			update_timer += delta

			# Debug
			Debug.clear()

			# Update
			self.update(delta)
			while update_timer >= self.fixed_time_rate:
				self.fixed_update()
				update_timer -= self.fixed_time_rate

			# Drawing
			Debug.update_timing_text(delta, round(self.clock.get_fps()))

			self.draw()
			Debug.draw()
			self.renderer.present()

			# Events
			self.handle_events()

			# State check
			self.switch_state()
