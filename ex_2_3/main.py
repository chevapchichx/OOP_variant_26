"""
Ферма «Ново-простоквашино» — главный модуль

Демонстрирует:
- Наследование и агрегацию в иерархии
- Инкапсуляцию с property
- Паттерн Мост для импорта
- Структуры данных: стек, дек
"""

import sys
from PyQt6.QtWidgets import QApplication
from view.main_window import MainWindow


def main():
    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
