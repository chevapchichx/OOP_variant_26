"""Род (Genus) - пятый таксономический ранг."""

from data.taxonomic_rank import TaxonomicRank
from data.family import Family


class Genus(TaxonomicRank):
    """Род. Агрегирует Семейство."""

    def __init__(self, name, family, description=""):
        super().__init__(name, description)
        self._family = family

    @property
    def family(self):
        return self._family

    def get_parent(self):
        return self._family

    def get_rank_name(self):
        return "Род"
