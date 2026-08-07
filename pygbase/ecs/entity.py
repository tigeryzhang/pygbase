from collections.abc import Mapping
from typing import TYPE_CHECKING, Any, ClassVar

if TYPE_CHECKING:
	from .component import Component


class Entity:
	default_components: ClassVar[Mapping[type[Component], tuple[Any, ...]]] = {}

	def __init__(self, entity_id: int):
		self.id = entity_id
