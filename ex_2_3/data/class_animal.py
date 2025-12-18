"""Класс (ClassAnimal) - второй таксономический ранг."""

from data.taxonomic_rank import TaxonomicRank
from data.phylum import Phylum


class ClassAnimal(TaxonomicRank):
    """Класс. Агрегирует Тип."""
    def __init__(self, name, phylum, description=""):
        super().__init__(name, description)
        self._phylum = phylum

    @property
    def phylum(self):
        return self._phylum

    def get_parent(self):
        return self._phylum

    def get_rank_name(self):
        return "Класс"
