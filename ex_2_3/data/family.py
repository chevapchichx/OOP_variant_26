"""Семейство (Family) - четвёртый таксономический ранг."""

from data.taxonomic_rank import TaxonomicRank
from data.order import Order


class Family(TaxonomicRank):
    """Семейство. Агрегирует Отряд."""

    def __init__(self, name, order, description=""):
        super().__init__(name, description)
        self._order = order

    @property
    def order(self):
        return self._order

    def get_parent(self):
        return self._order

    def get_rank_name(self):
        return "Семейство"
