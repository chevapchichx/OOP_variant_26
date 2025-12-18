"""Инициализация пакета data."""

from data.taxonomic_rank import TaxonomicRank
from data.phylum import Phylum
from data.class_animal import ClassAnimal
from data.order import Order
from data.family import Family
from data.genus import Genus
from data.species import Species
from data.animal import Animal
from data.farm import Farm

__all__ = [
    "TaxonomicRank",
    "Phylum",
    "ClassAnimal",
    "Order",
    "Family",
    "Genus",
    "Species",
    "Animal",
    "Farm",
]
