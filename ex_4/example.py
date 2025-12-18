"""
МОСТ (BRIDGE) - разделяет абстракцию и реализацию

Проблема:
Есть фигуры (Circle, Square) и цвета (Red, Blue)
При наследовании: RedCircle, BlueCircle, RedSquare... = комбинаторный взрыв
10 фигур × 10 цветов = 100 классов!!

Решение:
Две иерархии: Shape (абстракция) и Color (реализация)
Shape содержит ссылку на Color - это "мост"
"""

from abc import ABC, abstractmethod


# Реализация - интерфейс цвета
class Color(ABC):
    @abstractmethod
    def fill(self):
        pass


# Конкретные реализации
class Red(Color):
    def fill(self):
        return "красным"


class Blue(Color):
    def fill(self):
        return "синим"


class Green(Color):
    def fill(self):
        return "зелёным"


# Абстракция - фигура
class Shape(ABC):
    def __init__(self, color):
        self._color = color  # МОСТ

    @abstractmethod
    def draw(self):
        pass


# Расширенные абстракции
class Circle(Shape):
    def draw(self):
        return f"Круг закрашен {self._color.fill()}"


class Square(Shape):
    def draw(self):
        return f"Квадрат закрашен {self._color.fill()}"


class Triangle(Shape):
    def draw(self):
        return f"Треугольник закрашен {self._color.fill()}"



# Любая комбинация работает без отдельного класса
red_circle = Circle(Red())
blue_square = Square(Blue())
green_triangle = Triangle(Green())

print(red_circle.draw())
print(blue_square.draw())
print(green_triangle.draw())
