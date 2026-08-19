import pygame
import pygame._sdl2.video as sdl_video

from ..camera import Camera


class Shadow:
	shadow_texture: sdl_video.Texture

	def __init__(self, pos: pygame.typing.Point, size: float):
		self._linked_pos: bool
		if isinstance(pos, pygame.Vector2):
			self._linked_pos = True
			self.pos = pos
		else:
			self._linked_pos = False
			self.pos = pygame.Vector2(pos)

		self.size = size

	def update_pos(self, pos):
		if self._linked_pos:
			raise RuntimeError("Cannot modify linked position")

		self.pos.update(pos)

	def draw(self, camera: Camera | None):
		pos = self.pos if camera is None else camera.world_to_screen(self.pos)
		Shadow.shadow_texture.draw(dstrect=(pos, (self.size, self.size)))
