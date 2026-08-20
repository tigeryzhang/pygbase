import pygame

from pygbase.common import Common

from .. import Texture
from ..camera import Camera
from .image import Image


class SpriteSheet:
	def __init__(self, data: dict, resource_path: str, default_scale: float):
		# Data info
		self.n_rows: int = data["rows"]
		self.n_cols: int = data["columns"]
		self.scale: int = data["scale"] if data["scale"] != 0 else default_scale  # ty: ignore[invalid-assignment]
		self.rotatable: bool = data["rotatable"]
		self.tile_width: int = data["tile_width"] * self.scale
		self.tile_height: int = data["tile_height"] * self.scale

		# Load Sprite Sheet
		self.texture = Texture.from_surface(
			Common.renderer,
			pygame.image.load(resource_path),
		)

		# Automatically set n_rows and n_cols if needed
		if self.n_rows == 0:
			self.n_rows = int(self.texture.height / self.tile_height)
		if self.n_cols == 0:
			self.n_cols = int(self.texture.width / self.tile_width)

		self._images: list[Image] = []
		self._load_sprite_sheet()
		self.length = len(self._images)

	def _load_image(self, row, col):
		rect = pygame.Rect(
			col * self.tile_width,
			row * self.tile_height,
			self.tile_width,
			self.tile_height,
		)
		self._images.append(Image(self.texture, src_rect=rect))

	def _load_sprite_sheet(self):
		for row in range(self.n_rows):
			for col in range(self.n_cols):
				self._load_image(row, col)

	def get_image(self, index: int) -> Image:
		return self._images[index]

	def draw_sheet(self, camera: Camera):
		self.texture.draw(dstrect=(*camera.pos, self.texture.width, self.texture.height))
