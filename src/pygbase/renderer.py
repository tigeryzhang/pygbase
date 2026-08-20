from typing import Any, Literal, Self

import pygame
import pygame._sdl2.video as sdl


class Renderer(sdl.Renderer):
	def clear_with_color(self, color: pygame.typing.ColorLike):
		prev_color = self.draw_color
		self.draw_color = color
		self.clear()
		self.draw_color = prev_color

	def using_draw_color(self, color: pygame.typing.ColorLike) -> _RendererContextHelper:
		return _RendererContextHelper("draw_color", self, color)

	def using_blend_mode(self, blend_mode: int) -> _RendererContextHelper:
		return _RendererContextHelper("blend_mode", self, blend_mode)

	def using_target(self, target: sdl.Texture) -> _RendererContextHelper:
		return _RendererContextHelper("target", self, target)


class _RendererContextHelper:
	def __init__(self, renderer_field: Literal["draw_color", "blend_mode", "target"], renderer: Renderer, value: Any):
		self._renderer_field = renderer_field
		self._renderer = renderer
		self._value = value
		self._prev_value: Any

	def __enter__(self) -> Self:
		if self._renderer_field == "draw_color":
			self._prev_value = self._renderer.draw_color
			self._renderer.draw_color = self._value
		elif self._renderer_field == "blend_mode":
			self._prev_value = self._renderer.draw_blend_mode
			self._renderer.draw_blend_mode = self._value
		elif self._renderer_field == "target":
			self._prev_value = self._renderer.target
			self._renderer.target = self._value

		return self

	def __exit__(self, *args) -> bool:
		if self._renderer_field == "draw_color":
			self._renderer.draw_color = self._prev_value
		if self._renderer_field == "blend_mode":
			self._renderer.draw_blend_mode = self._prev_value
		if self._renderer_field == "target":
			self._renderer.target = self._prev_value

		return False
