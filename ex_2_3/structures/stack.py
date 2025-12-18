"""
Стек (LIFO) - Last In, First Out

Последний добавленный элемент извлекается первым.
Используется для истории просмотров (кнопка "Назад").

Реализация на основе связного списка.
"""


class _Node:
    """Узел связного списка."""

    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:
    """Стек на основе связного списка."""

    def __init__(self):
        self.__top = None
        self.__size = 0

    def push(self, item):
        """Добавить на вершину."""
        new_node = _Node(item)
        new_node.next = self.__top
        self.__top = new_node
        self.__size += 1

    def pop(self):
        """Извлечь с вершины."""
        if self.is_empty():
            return None
        data = self.__top.data
        self.__top = self.__top.next
        self.__size -= 1
        return data

    def peek(self):
        """Вершина без удаления."""
        if self.is_empty():
            return None
        return self.__top.data

    def is_empty(self):
        """Пуст ли стек."""
        return self.__top is None

    def size(self):
        """Размер стека."""
        return self.__size

    def clear(self):
        """Очистить стек."""
        self.__top = None
        self.__size = 0

    def __len__(self):
        return self.__size
