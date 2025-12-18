"""Тип (Phylum) - первый таксономический ранг."""

from data.taxonomic_rank import TaxonomicRank


class Phylum(TaxonomicRank):
    """Тип - корень иерархии."""

    def __init__(self, name, description=""):
        super().__init__(name, description)

    def get_parent(self):
        return None  # Тип - корень

    def get_rank_name(self):
        return "Тип"
