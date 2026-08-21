import pygame

from .common import Common


class Scene:
	child_state_id = 1

	def __init_subclass__(cls, **kwargs):
		if "name" not in kwargs:
			raise KeyError(
				'"name" keyword argument not in class definition. It should look like <class Child(GameState, name="child")>'
			)

		name = kwargs["name"]

		# Add id to common and child class, then increment by 1
		Common.add_scene(name, Scene.child_state_id)
		cls.id = Scene.child_state_id

		Scene.child_state_id += 1

	def __init__(self, clear_color: pygame.typing.ColorLike | None = (0, 0, 0)):
		self._next_state = self
		self.clear_color = clear_color

	def enter(self):
		"""Called when entering state"""

	def exit(self):
		"""Called when exiting state"""

	def set_next_state(self, next_state: Scene):
		self._next_state = next_state

	def set_next_state_type(self, next_state: type[Scene], args: tuple):
		if len(args) > 0:
			self._next_state = next_state(*args)
		else:
			self._next_state = next_state()

	def get_next_state(self) -> Scene:
		return self._next_state

	def update(self, delta: float):
		pass

	def fixed_update(self, delta: float):
		pass

	def draw(self):
		pass
