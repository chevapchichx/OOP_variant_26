"""Ферма - контейнер для животных."""

from data.animal import Animal


class Farm:
    """Ферма - хранит список животных."""

    def __init__(self, name="Ферма"):
        self._name = name
        self._animals = []

    @property
    def name(self):
        return self._name

    @property
    def animals(self):
        return self._animals.copy()

    def add_animal(self, animal):
        """Добавить животное."""
        if isinstance(animal, Animal):
            self._animals.append(animal)

    def get_by_name(self, name):
        """Найти по кличке."""
        for animal in self._animals:
            if animal.name == name:
                return animal
        return None

    def count(self):
        """Количество животных."""
        return len(self._animals)

    def clear(self):
        """Очистить ферму."""
        self._animals.clear()

    def __len__(self):
        return len(self._animals)

    def __iter__(self):
        return iter(self._animals)
