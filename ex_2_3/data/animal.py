"""
Животное (Animal) - конкретный обитатель фермы

Демонстрирует Инкапсуляцию:
- private атрибуты (__age, __weight) с валидацией
- property для контролируемого доступа
"""

from data.taxonomic_rank import TaxonomicRank
from data.species import Species


class Animal(TaxonomicRank):
    """Животное - агрегирует Вид + личные характеристики."""
    def __init__(self, name, species, age=0, weight=0.0, description=""):
        super().__init__(name, description)
        self._species = species
        self.__age = 0
        self.__weight = 0.0
        # Валидация через сеттеры
        self.age = age
        self.weight = weight

    @property
    def species(self):
        return self._species

    @property
    def age(self):
        return self.__age

    @age.setter
    def age(self, value):
        """Сеттер с валидацией."""
        if not isinstance(value, (int, float)):
            raise TypeError("Возраст должен быть числом")
        if value < 0:
            raise ValueError("Возраст не может быть отрицательным")
        if value > 100:
            raise ValueError("Возраст слишком большой")
        self.__age = int(value)

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self, value):
        """Сеттер с валидацией."""
        if not isinstance(value, (int, float)):
            raise TypeError("Вес должен быть числом")
        if value < 0:
            raise ValueError("Вес не может быть отрицательным")
        self.__weight = float(value)

    def get_parent(self):
        return self._species

    def get_rank_name(self):
        return "Животное"

    def to_dict(self):
        """Экспорт в словарь."""
        return {
            "name": self._name,
            "species": self._species.name if self._species else "",
            "genus": self._species.genus.name if self._species else "",
            "family": self._species.genus.family.name if self._species else "",
            "order": self._species.genus.family.order.name if self._species else "",
            "class": self._species.genus.family.order.class_animal.name if self._species else "",
            "phylum": self._species.genus.family.order.class_animal.phylum.name if self._species else "",
            "age": self.__age,
            "weight": self.__weight,
            "description": self._description
        }

    def __str__(self):
        return f"{self._name} ({self._species.name if self._species else '?'}), {self.__age} лет"
