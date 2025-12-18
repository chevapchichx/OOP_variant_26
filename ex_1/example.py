"""
ИНКАПСУЛЯЦИЯ - сокрытие данных и контроль доступа

Проблема:
Без инкапсуляции данные можно изменить как угодно
person.age = -100  # Некорректное состояние!

Решение:
Скрыть данные и дать доступ через property с валидацией
"""

# Защита на уровне объекта

class Person:
    def __init__(self, name, age):
        self._name = name      # protected - для наследников
        self.__age = age       # private - только внутри класса

    # Геттер через @property
    @property
    def age(self):
        return self.__age
    
    @property
    def name(self):
        return self._name

    # Сеттер с валидацией
    @age.setter
    def age(self, value):
        if value < 0:
            raise ValueError("Возраст не может быть отрицательным!")
        if value > 150:
            raise ValueError("Возраст слишком большой!")
        self.__age = value


person = Person("Иван", 25)
print(f"Имя: {person.name}, Возраст: {person.age}")

person.age = 30  # Работает через сеттер
print(f"Новый возраст: {person.age}")

# person.age = -5  # ValueError: Возраст не может быть отрицательным!



# Защита на уровне класса

class Counter:
    __count = 0  # Приватный атрибут класса

    def __init__(self):
        Counter.__count += 1

    @classmethod
    def get_count(cls):
        """Доступ к приватному атрибуту класса через classmethod"""
        return cls.__count

    @staticmethod
    def description():
        """Статический метод - не имеет доступа к приватным атрибутам"""
        return "Счётчик созданных объектов"


c1 = Counter()
c2 = Counter()
c3 = Counter()

print(f"\n{Counter.description()}: {Counter.get_count()}")
