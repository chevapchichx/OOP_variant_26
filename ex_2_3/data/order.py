"""Отряд (Order) - третий таксономический ранг."""

from data.taxonomic_rank import TaxonomicRank
from data.class_animal import ClassAnimal


class Order(TaxonomicRank):
    """Отряд. Агрегирует Класс."""

    def __init__(self, name, class_animal, description=""):
        super().__init__(name, description)
        self._class_animal = class_animal

    @property
    def class_animal(self):
        return self._class_animal

    def get_parent(self):
        return self._class_animal

    def get_rank_name(self):
        return "Отряд"
