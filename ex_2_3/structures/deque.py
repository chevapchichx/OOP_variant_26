"""
Deque (Double-Ended Queue) - двусторонняя очередь

Добавление и удаление с обоих концов.
Используется для навигации вперёд/назад.

Реализация на основе двусвязного списка.
"""


class _Node:
    """Узел двусвязного списка."""

    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class Deque:
    """Дек на основе двусвязного списка."""

    def __init__(self):
        self.__head = None  # Начало (front)
        self.__tail = None  # Конец (back)
        self.__size = 0

    def push_front(self, item):
        """Добавить в начало."""
        new_node = _Node(item)
        if self.is_empty():
            self.__head = new_node
            self.__tail = new_node
        else:
            new_node.next = self.__head
            self.__head.prev = new_node
            self.__head = new_node
        self.__size += 1

    def push_back(self, item):
        """Добавить в конец."""
        new_node = _Node(item)
        if self.is_empty():
            self.__head = new_node
            self.__tail = new_node
        else:
            new_node.prev = self.__tail
            self.__tail.next = new_node
            self.__tail = new_node
        self.__size += 1

    def pop_front(self):
        """Извлечь из начала."""
        if self.is_empty():
            return None
        data = self.__head.data
        self.__head = self.__head.next
        if self.__head is None:
            self.__tail = None
        else:
            self.__head.prev = None
        self.__size -= 1
        return data

    def pop_back(self):
        """Извлечь из конца."""
        if self.is_empty():
            return None
        data = self.__tail.data
        self.__tail = self.__tail.prev
        if self.__tail is None:
            self.__head = None
        else:
            self.__tail.next = None
        self.__size -= 1
        return data

    def front(self):
        """Первый элемент без удаления."""
        if self.is_empty():
            return None
        return self.__head.data

    def back(self):
        """Последний элемент без удаления."""
        if self.is_empty():
            return None
        return self.__tail.data

    def is_empty(self):
        """Пуст ли дек."""
        return self.__head is None

    def size(self):
        """Размер дека."""
        return self.__size

    def clear(self):
        """Очистить дек."""
        self.__head = None
        self.__tail = None
        self.__size = 0

    def to_list(self):
        """Получить элементы как список (для совместимости)."""
        result = []
        current = self.__head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result

    def __len__(self):
        return self.__size
