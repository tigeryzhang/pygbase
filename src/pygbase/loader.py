from collections.abc import Callable

from .resources import Resources
from .scene import Scene


class Loading(Scene, name="_loading"):
	def __init__(
		self,
		after_load_state: type[Scene],
		run_on_load_complete: tuple[Callable, ...],
	):
		super().__init__(clear_color=(0, 0, 0))

		Resources.init_load()

		self.after_load_state = after_load_state
		self.run_on_load_complete = run_on_load_complete

	def update(self, delta: float):
		if Resources.load_update():  # Done loading
			for func in self.run_on_load_complete:
				func()

			self.set_next_state(self.after_load_state())
