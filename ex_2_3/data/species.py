"""Вид (Species) - шестой таксономический ранг."""

from data.taxonomic_rank import TaxonomicRank
from data.genus import Genus


class Species(TaxonomicRank):
    """Вид. Агрегирует Род."""

    def __init__(self, name, genus, description=""):
        super().__init__(name, description)
        self._genus = genus

    @property
    def genus(self):
        return self._genus

    def get_parent(self):
        return self._genus

    def get_rank_name(self):
        return "Вид"
