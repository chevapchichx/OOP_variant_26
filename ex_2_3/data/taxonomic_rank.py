"""
Таксономический ранг - базовый класс

Демонстрирует Инкапсуляцию:
- protected атрибуты (_name) для наследников
- private атрибуты (__id) скрыты полностью
- property для контролируемого доступа
"""

from abc import ABC, abstractmethod


class TaxonomicRank(ABC):
    """Абстрактный базовый класс таксономии."""

    __id_counter = 0  # private атрибут класса

    def __init__(self, name, description=""):
        self._name = name
        self._description = description
        self.__id = TaxonomicRank.__id_counter
        TaxonomicRank.__id_counter += 1

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or not isinstance(value, str):
            raise ValueError("Имя должно быть непустой строкой")
        self._name = value

    @property
    def description(self):
        return self._description

    @description.setter
    def description(self, value):
        self._description = str(value) if value else ""

    @property
    def id(self):
        """Только чтение - нет сеттера."""
        return self.__id

    @abstractmethod
    def get_parent(self):
        """Получить родительский ранг."""
        pass

    @abstractmethod
    def get_rank_name(self):
        """Название ранга"""
        pass

    def get_full_hierarchy(self):
        """Полная иерархия от текущего до корня."""
        hierarchy = [(self.get_rank_name(), self._name)]
        parent = self.get_parent()
        while parent:
            hierarchy.append((parent.get_rank_name(), parent.name))
            parent = parent.get_parent()
        return list(reversed(hierarchy))

    def __str__(self):
        return f"{self.get_rank_name()}: {self._name}"

    def __repr__(self):
        return f"{self.__class__.__name__}('{self._name}')"
