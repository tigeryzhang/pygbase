from collections.abc import Callable

from .game_state import GameState
from .resources import Resources


class Loading(GameState, name="loading"):
	def __init__(
		self,
		after_load_state: type[GameState],
		run_on_load_complete: tuple[Callable, ...],
	):
		# From GameState, but no parent __init__ call, so have to do it manually
		self.id = -1
		self._next_state = self
		self.clear_color = (0, 0, 0)

		Resources.init_load()

		self.after_load_state = after_load_state
		self.run_on_load_complete = run_on_load_complete

	def update(self, delta: float):
		if Resources.load_update():  # Done loading
			for func in self.run_on_load_complete:
				func()

			self.set_next_state(self.after_load_state())
