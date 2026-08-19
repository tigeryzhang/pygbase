from typing import Literal

import pygame
import pygame._sdl2.video as sdl_video

from .common import Common


# TODO: Switch away from static class
class Debug:
	_active: bool = False

	_renderer: sdl_video.Renderer

	_debug_operations: list[tuple[Literal["rect", "circle", "line"], *tuple]] = []

	_show_timing_debug: bool = False
	_timing_font: pygame.font.Font
	_timing_surf: pygame.Surface

	@classmethod
	def init(cls):
		cls._renderer = Common.get("renderer")
		cls._timing_font: pygame.font.Font = pygame.font.SysFont("arial", 30)

	@classmethod
	def show(cls):
		cls._active = True

	@classmethod
	def hide(cls):
		cls._active = False

	@classmethod
	def toggle(cls):
		cls._active = not cls._active

	@classmethod
	def show_fps(cls):
		cls._show_timing_debug = True

	@classmethod
	def hide_fps(cls):
		cls._show_timing_debug = False

	@classmethod
	def toggle_fps(cls):
		cls._show_timing_debug = not cls._show_timing_debug

	@classmethod
	def is_active(cls) -> bool:
		return cls._active

	@classmethod
	def clear(cls) -> None:
		"""
		Called at the beginning of a frame to clear the debug surface
		"""
		cls._debug_operations.clear()

	@classmethod
	def update_timing_text(
		cls,
		delta: float,
		fps: float,
	):
		if cls._show_timing_debug:
			cls._timing_surf = cls._timing_font.render(f"fps: {fps}, delta: {delta}", True, "yellow")

	@classmethod
	def draw_rect(
		cls,
		rect: pygame.typing.RectLike,
		color: pygame.typing.ColorLike,
		width: int = 1,
	):
		if cls._active:
			cls._debug_operations.append(("rect", rect, color, width))

	@classmethod
	def draw_circle(
		cls,
		center: pygame.typing.Point,
		radius: float,
		color: pygame.typing.ColorLike,
		width: int = 1,
	):
		if cls._active:
			cls._debug_operations.append(("circle", center, radius, color, width))

	@classmethod
	def draw_line(
		cls,
		start: pygame.typing.Point,
		end: pygame.typing.Point,
		color: pygame.typing.ColorLike,
		width: int = 1,
	):
		if cls._active:
			cls._debug_operations.append(("line", start, end, color, width))

	@classmethod
	def draw(cls) -> None:
		"""
		Called at end of frame on top of everything
		"""
		# TODO: Add support for line width
		if cls._active:
			for operation in cls._debug_operations:
				if operation[0] == "rect":
					cls._renderer.draw_color = operation[2]
					cls._renderer.draw_rect(operation[1])
				elif operation[0] == "line":
					cls._renderer.draw_blend_mode = operation[3]
					cls._renderer.draw_line(operation[1], operation[2])
				elif operation[0] == "circle":
					pass
				else:
					raise ValueError("Unsupported debug type")

		if cls._show_timing_debug:
			rect = cls._timing_surf.get_rect(topright=(Common.get("screen_width") - 20, 20))
			timing_texture = sdl_video.Texture.from_surface(cls._renderer, cls._timing_surf)
			timing_texture.draw(dstrect=rect)
