from typing import Literal

import pygame

from .. import Texture
from ..common import Common


class Image:
	def __init__(
		self,
		image: str | pygame.Surface | Texture,
		src_rect: pygame.Rect | None = None,
		scale: float = 1,
	):
		if isinstance(image, str):
			image = pygame.image.load(image)

		if isinstance(image, Texture):
			self._texture = image
		else:
			self._texture = Texture.from_surface(
				Common.renderer,
				image,
			)

		self.src_rect = src_rect
		self.scale = scale

	@property
	def width(self) -> int:
		return int(self._texture.width * self.scale)

	@property
	def height(self) -> int:
		return int(self._texture.height * self.scale)

	def set_blend_mode(self, blend_mode: int):
		self._texture.blend_mode = blend_mode

	def draw(
		self,
		pos: pygame.Vector2 | tuple[float, float],
		scale: float | tuple[int, int] | None = None,
		angle: float = 0,
		pivot_point: tuple[int, int] = (0, 0),  # TODO: Consider adjusting with scale
		flip: tuple[bool, bool] = (False, False),
		draw_pos: Literal["topleft", "center", "midbottom"] | None = None,
	):
		if scale is None:
			scale = self.scale

		if isinstance(scale, float | int):
			scale = (int(self._texture.width * scale), int(self._texture.height * scale))

		rect = pygame.Rect(pos, scale)

		if draw_pos is not None:
			if draw_pos == "topleft":
				rect.topleft = pos
			elif draw_pos == "center":
				rect.center = pos
			elif draw_pos == "midbottom":
				rect.midbottom = pos
			else:
				raise ValueError(f"{draw_pos} not a valid position.")

		self._texture.draw(
			srcrect=self.src_rect,
			dstrect=rect,
			angle=angle,
			origin=pivot_point,
			flip_x=flip[0],
			flip_y=flip[1],
		)
