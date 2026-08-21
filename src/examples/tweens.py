import pygbase
from pygbase.common import Common
from pygbase.ui import *


class Tweens(pygbase.Scene, name="tweens"):
	def __init__(self):
		super().__init__(clear_color=(20, 20, 20))
		self.renderer = Common.renderer

		from .menu import Menu

		with Button(
			self.set_next_state_type,
			callback_args=(Menu, ()),
			pos=(10, 10),
			size=(150, Fit()),
		) as ui:
			with Image(
				"image/button",
				size=(Grow(), Fit()),
				x_align=XAlign.CENTER,
				y_align=YAlign.CENTER,
			):
				Text("Back", 20, "white")

		ui.resolve_layout(pygbase.Common.get("screen_size"))
		self.ui = ui

		self.tween_time = 3
		self.tween_values = (0, 0.2, 0.7, 1)

		self.tweens = [
			pygbase.LinearTween(self.tween_values, self.tween_time),
			pygbase.CubicTween(self.tween_values, self.tween_time),
		]

	def update(self, delta: float):
		self.ui.update(delta)

		for tween in self.tweens:
			tween.tick(delta)

			if tween.value() == self.tween_values[-1]:
				tween.progress = 0

	def draw(self):
		prev_draw_color = self.renderer.draw_color
		for tween_value in self.tween_values:
			self.renderer.draw_color = (50, 50, 50)
			self.renderer.draw_line(
				(40 + (800 - 120) * tween_value, 100),
				(40 + (800 - 120) * tween_value, 700),
			)

		for index, tween in enumerate(self.tweens):
			self.renderer.draw_color = "light blue"
			self.renderer.draw_line(
				(40, 150 + 50 * index),
				(800 - 80, 150 + 50 * index),
			)

			# TODO: How big is a point? Need some way to draw circles
			self.renderer.draw_color = "yellow"
			self.renderer.fill_rect(
				(
					(
						40 + (800 - 120) * tween.value() - 5,
						150 + 50 * index - 5,
					),
					(10, 10),
				),
			)
		self.renderer.draw_color = prev_draw_color

		self.ui.draw()
