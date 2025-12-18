"""
ФЕРМА - главное окно приложения

Демонстрирует все структуры данных:
- Stack (LIFO) - история просмотров (кнопка "Назад")
- Deque - обычное и приоритетное кормление (обычное в конец, срочное в начало)
- Паттерн Мост - импорт данных в разных форматах
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
    QListWidget, QLabel, QComboBox,
    QGroupBox, QFileDialog, QTreeWidget, QTreeWidgetItem,
    QSplitter, QListWidgetItem, QProgressBar
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QFont

from structures import Stack, Deque
from export.formats import JsonFormat, CsvFormat, TxtFormat
from data import Phylum, ClassAnimal, Order, Family, Genus, Species, Animal, Farm


ANIMAL_ICONS = {
    'корова': '🐄',
    'кошка': '🐱',
    'собака': '🐕',
    'курица': '🐔',
}


def get_animal_icon(species_name):
    """Эмодзи по виду животного."""
    species_lower = species_name.lower()
    for key, icon in ANIMAL_ICONS.items():
        if key in species_lower:
            return icon
    return '🐾'


def create_sample_animals():
    """Создание примеров животных с полной иерархией."""
    chordata = Phylum("Хордовые", "Животные с хордой")

    mammals = ClassAnimal("Млекопитающие", chordata, "Теплокровные с шерстью")
    birds = ClassAnimal("Птицы", chordata, "Теплокровные с перьями")

    carnivora = Order("Хищные", mammals, "Плотоядные млекопитающие")
    artiodactyla = Order("Парнокопытные", mammals, "Копытные")
    galliformes = Order("Курообразные", birds, "Наземные птицы")

    felidae = Family("Кошачьи", carnivora, "Семейство кошачьих")
    canidae = Family("Псовые", carnivora, "Семейство псовых")
    bovidae = Family("Полорогие", artiodactyla, "Рогатый скот")
    phasianidae = Family("Фазановые", galliformes, "Куры и фазаны")

    felis = Genus("Кошки", felidae, "Род мелких кошачьих")
    canis = Genus("Волки", canidae, "Род волков и собак")
    bos = Genus("Быки", bovidae, "Род быков")
    gallus = Genus("Куры", phasianidae, "Род домашних кур")

    cat_species = Species("Домашняя кошка", felis, "Felis catus")
    dog_species = Species("Домашняя собака", canis, "Canis familiaris")
    cow_species = Species("Домашняя корова", bos, "Bos taurus")
    chicken_species = Species("Домашняя курица", gallus, "Gallus domesticus")

    animals = [
        Animal("Мурка", cow_species, 5, 450.0, "Рыжая корова"),
        Animal("Матроскин", cat_species, 3, 4.5, "Полосатый кот"),
        Animal("Шарик", dog_species, 4, 15.0, "Охотничий пёс"),
        Animal("Пеструшка", chicken_species, 2, 2.0, "Несушка"),
    ]

    return animals


class MainWindow(QWidget):
    """Основное окно фермы."""

    def __init__(self):
        super().__init__()
        self.farm = Farm("Ново-Простоквашино")

        self.feeding_deque = Deque()
        self.view_history = Stack()

        self._init_ui()

    def _init_ui(self):
        """Создание интерфейса."""
        self.setWindowTitle(f"🐄 Ферма «{self.farm.name}»")
        self.setMinimumSize(1000, 700)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(main_layout)

        title = QLabel(f"🏡 Ферма «{self.farm.name}»")
        title.setFont(QFont('Arial', 28, QFont.Weight.Bold))
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet(
            "padding: 20px 15px; border-bottom: 2px solid #333;")
        title.setMinimumHeight(70)
        main_layout.addWidget(title, stretch=0)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 1)
        main_layout.addWidget(splitter, stretch=1)

        left_panel = self._create_left_panel()
        splitter.addWidget(left_panel)

        right_panel = self._create_right_panel()
        splitter.addWidget(right_panel)

        splitter.setSizes([450, 950])

    def _create_left_panel(self):
        """Левая панель - импорт и список."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)
        layout.setContentsMargins(15, 15, 15, 15)

        import_group = QGroupBox("📂 Импорт данных (Паттерн Мост)")
        import_group.setFont(QFont('Arial', 13, QFont.Weight.Bold))
        import_layout = QHBoxLayout()
        import_layout.setSpacing(12)
        import_group.setLayout(import_layout)

        self.format_combo = QComboBox()
        self.format_combo.addItems(
            ["Выберите формат", "Пример данных", "JSON", "CSV", "TXT"])
        self.format_combo.setFont(QFont('Arial', 12))
        self.format_combo.setMinimumHeight(40)
        self.format_combo.currentTextChanged.connect(self._on_format_changed)
        self.format_combo.model().item(0).setEnabled(False)
        import_layout.addWidget(self.format_combo)

        self.import_btn = QPushButton("📁 Загрузить")
        self.import_btn.setFont(QFont('Arial', 12))
        self.import_btn.setMinimumHeight(40)
        self.import_btn.setMinimumWidth(120)
        self.import_btn.setEnabled(False)
        self.import_btn.clicked.connect(self._import_data)
        import_layout.addWidget(self.import_btn)

        layout.addWidget(import_group, stretch=0)

        animals_group = QGroupBox("🐾 Животные фермы")
        animals_group.setFont(QFont('Arial', 13, QFont.Weight.Bold))
        animals_layout = QVBoxLayout()
        animals_layout.setSpacing(15)
        animals_group.setLayout(animals_layout)

        self.animals_list = QListWidget()
        self.animals_list.setFont(QFont('Arial', 14))
        self.animals_list.setSpacing(3)
        self.animals_list.itemClicked.connect(self._on_animal_selected)
        self.animals_list.setMinimumHeight(300)
        animals_layout.addWidget(self.animals_list, stretch=1)

        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(12)

        self.feed_btn = QPushButton("🍽 В очередь")
        self.feed_btn.clicked.connect(self._add_to_feeding_normal)
        self.feed_btn.setFont(QFont('Arial', 12))
        self.feed_btn.setMinimumHeight(40)
        self.feed_btn.setToolTip(
            "Добавить в конец очереди (обычное кормление)")
        self.feed_btn.setEnabled(False)
        btn_layout.addWidget(self.feed_btn)

        self.urgent_btn = QPushButton("🚨 Срочно!")
        self.urgent_btn.clicked.connect(self._add_to_feeding_urgent)
        self.urgent_btn.setFont(QFont('Arial', 12))
        self.urgent_btn.setMinimumHeight(40)
        self.urgent_btn.setToolTip("Добавить в НАЧАЛО очереди (приоритет)")
        self.urgent_btn.setEnabled(False)
        btn_layout.addWidget(self.urgent_btn)

        animals_layout.addLayout(btn_layout, stretch=0)

        btn_layout2 = QHBoxLayout()
        btn_layout2.setSpacing(12)

        self.clear_btn = QPushButton("🗑 Очистить")
        self.clear_btn.clicked.connect(self._clear_all_animals)
        self.clear_btn.setFont(QFont('Arial', 12))
        self.clear_btn.setMinimumHeight(40)
        self.clear_btn.setEnabled(False)
        btn_layout2.addWidget(self.clear_btn)

        animals_layout.addLayout(btn_layout2, stretch=0)
        layout.addWidget(animals_group, stretch=1)

        return panel

    def _create_right_panel(self):
        """Правая панель - иерархия, история и кормление."""
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setSpacing(20)
        layout.setContentsMargins(15, 15, 15, 15)

        tree_group = QGroupBox(
            "🌳 Иерархия (Агрегация, Наследование) + История (Стек LIFO)")
        tree_group.setFont(QFont('Arial', 13, QFont.Weight.Bold))
        tree_layout = QVBoxLayout()
        tree_layout.setSpacing(12)
        tree_group.setLayout(tree_layout)

        history_layout = QHBoxLayout()
        history_layout.setSpacing(12)

        self.back_btn = QPushButton("⬅ Назад")
        self.back_btn.setFont(QFont('Arial', 12))
        self.back_btn.setMinimumHeight(40)
        self.back_btn.setMaximumWidth(100)
        self.back_btn.clicked.connect(self._go_back_in_history)
        self.back_btn.setEnabled(False)
        self.back_btn.setToolTip(
            "Вернуться к предыдущему животному (Стек LIFO)")
        history_layout.addWidget(self.back_btn)

        self.history_label = QLabel("История: пусто")
        self.history_label.setFont(QFont('Arial', 13))
        self.history_label.setStyleSheet("color: #666;")
        history_layout.addWidget(self.history_label)
        history_layout.addStretch()

        tree_layout.addLayout(history_layout, stretch=0)

        self.tree_widget = QTreeWidget()
        self.tree_widget.setHeaderLabels(["Таксономический ранг"])
        self.tree_widget.setFont(QFont('Arial', 12))
        self.tree_widget.setAnimated(True)
        self.tree_widget.setIndentation(30)
        tree_layout.addWidget(self.tree_widget, stretch=1)

        layout.addWidget(tree_group, stretch=1)

        feed_group = QGroupBox(
            "🍽 Очередь кормления (Deque - двусторонняя очередь)")
        feed_group.setFont(QFont('Arial', 13, QFont.Weight.Bold))
        feed_layout = QVBoxLayout()
        feed_layout.setSpacing(12)
        feed_group.setLayout(feed_layout)

        deque_info = QLabel(
            "💡 Deque: обычные → в конец, срочные → в начало"
        )
        deque_info.setStyleSheet("color: #666; font-size: 13px;")
        feed_layout.addWidget(deque_info)

        self.feed_list = QListWidget()
        self.feed_list.setFont(QFont('Arial', 12))
        self.feed_list.setMinimumHeight(120)
        feed_layout.addWidget(self.feed_list, stretch=1)

        self.feed_progress = QProgressBar()
        self.feed_progress.setMaximum(100)
        self.feed_progress.setValue(0)
        self.feed_progress.setFormat("Готов к кормлению")
        self.feed_progress.setFont(QFont('Arial', 11))
        self.feed_progress.setMinimumHeight(30)
        feed_layout.addWidget(self.feed_progress, stretch=0)

        self.feed_next_btn = QPushButton("✓ Накормить следующего")
        self.feed_next_btn.setFont(QFont('Arial', 12))
        self.feed_next_btn.setMinimumHeight(40)
        self.feed_next_btn.clicked.connect(self._feed_next)
        self.feed_next_btn.setEnabled(False)
        feed_layout.addWidget(self.feed_next_btn, stretch=0)

        layout.addWidget(feed_group, stretch=1)

        return panel

    def _on_format_changed(self, text):
        """Активация кнопки при выборе формата."""
        self.import_btn.setEnabled(text != "Выберите формат")

    def _load_sample_data(self):
        """Загрузка примеров."""
        animals = create_sample_animals()
        for animal in animals:
            self.farm.add_animal(animal)
        self._update_list()

    def _clear_all_animals(self):
        """Очистка всех данных."""
        self.farm.clear()
        self._update_list()
        self.tree_widget.clear()

        while not self.feeding_deque.is_empty():
            self.feeding_deque.pop_front()
        self._update_feed_list()

        while not self.view_history.is_empty():
            self.view_history.pop()
        self._update_history_label()

    def _import_data(self):
        """Импорт данных - паттерн мост"""
        format_name = self.format_combo.currentText()

        if format_name == "Пример данных":
            self._load_sample_data()
            return

        if format_name == "JSON":
            fmt = JsonFormat()
        elif format_name == "CSV":
            fmt = CsvFormat()
        elif format_name == "TXT":
            fmt = TxtFormat()
        else:
            return

        filepath, _ = QFileDialog.getOpenFileName(
            self, f"Открыть {format_name} файл", "",
            f"Файлы (*{fmt.get_extension()})"
        )

        if filepath:
            data = fmt.import_data(filepath)
            if data:
                for item in data:
                    animal = self._dict_to_animal(item)
                    if animal:
                        self.farm.add_animal(animal)
                self._update_list()

    def _dict_to_animal(self, data):
        """Конвертация словаря в объект Animal."""
        try:
            phylum = Phylum(data.get('phylum', 'Неизвестно'))
            class_animal = ClassAnimal(data.get('class', 'Неизвестно'), phylum)
            order = Order(data.get('order', 'Неизвестно'), class_animal)
            family = Family(data.get('family', 'Неизвестно'), order)
            genus = Genus(data.get('genus', 'Неизвестно'), family)
            species = Species(data.get('species', 'Неизвестно'), genus)

            age = data.get('age', 0)
            if isinstance(age, str):
                age = int(age) if age else 0

            weight = data.get('weight', 0.0)
            if isinstance(weight, str):
                weight = float(weight) if weight else 0.0

            animal = Animal(
                data.get('name', 'Безымянный'),
                species,
                age,
                weight,
                data.get('description', '')
            )
            return animal
        except Exception:
            return None

    def _update_list(self):
        """Обновление списка животных."""
        self.animals_list.clear()
        for animal in self.farm:
            icon = get_animal_icon(animal.species.name)
            item = QListWidgetItem(f"{icon} {animal.name}")
            self.animals_list.addItem(item)
        self._update_buttons_state()

    def _on_animal_selected(self, item):
        """Клик по животному - показ иерархии + запись в Stack."""
        idx = self.animals_list.row(item)
        animals = list(self.farm)
        if 0 <= idx < len(animals):
            animal = animals[idx]

            self.view_history.push(animal.name)
            self._update_history_label()

            self._show_hierarchy_for(animal)
            self._update_buttons_state()

    def _go_back_in_history(self):
        """Stack: вернуться к предыдущему животному."""
        if self.view_history.is_empty():
            return

        self.view_history.pop()

        if self.view_history.is_empty():
            self.tree_widget.clear()
            self._update_history_label()
            return

        prev_name = self.view_history.peek()
        animal = self.farm.get_by_name(prev_name)
        if animal:
            self._show_hierarchy_for(animal)

        self._update_history_label()

    def _update_history_label(self):
        """Обновление отображения истории."""
        if self.view_history.is_empty():
            self.history_label.setText("История: пусто")
            self.back_btn.setEnabled(False)
        else:
            count = self.view_history.size()
            current = self.view_history.peek()
            self.history_label.setText(
                f"История: {count} | Текущий: {current}")
            self.back_btn.setEnabled(count > 1)

    def _update_buttons_state(self):
        """Управление состоянием кнопок в зависимости от данных."""
        has_animals = self.farm.count() > 0
        animal_selected = self.animals_list.currentRow() >= 0
        queue_has_items = not self.feeding_deque.is_empty()

        self.feed_btn.setEnabled(has_animals and animal_selected)
        self.urgent_btn.setEnabled(has_animals and animal_selected)
        self.clear_btn.setEnabled(has_animals)
        self.feed_next_btn.setEnabled(queue_has_items)

    def _show_hierarchy_for(self, animal):
        """Построение дерева иерархии."""
        self.tree_widget.clear()

        icon = get_animal_icon(animal.species.name)

        species = animal.species
        genus = species.genus
        family = genus.family
        order = family.order
        class_animal = order.class_animal
        phylum = class_animal.phylum

        phylum_item = QTreeWidgetItem([f"🔬 Тип: {phylum.name}"])
        phylum_item.setFont(0, QFont('Arial', 13, QFont.Weight.Bold))

        class_item = QTreeWidgetItem([f"🦴 Класс: {class_animal.name}"])
        phylum_item.addChild(class_item)

        order_item = QTreeWidgetItem([f"📂 Отряд: {order.name}"])
        class_item.addChild(order_item)

        family_item = QTreeWidgetItem([f"👪 Семейство: {family.name}"])
        order_item.addChild(family_item)

        genus_item = QTreeWidgetItem([f"🧬 Род: {genus.name}"])
        family_item.addChild(genus_item)

        species_item = QTreeWidgetItem([f"🐾 Вид: {species.name}"])
        genus_item.addChild(species_item)

        animal_item = QTreeWidgetItem([
            f"{icon} {animal.name} — {animal.age} лет, {animal.weight} кг"
        ])
        animal_item.setFont(0, QFont('Arial', 14, QFont.Weight.Bold))
        species_item.addChild(animal_item)

        self.tree_widget.addTopLevelItem(phylum_item)
        self.tree_widget.expandAll()

    def _add_to_feeding_normal(self):
        """deque - добавление в конец очереди (обычное кормление)."""
        idx = self.animals_list.currentRow()
        animals = list(self.farm)
        if idx < 0 or idx >= len(animals):
            return

        animal = animals[idx]
        icon = get_animal_icon(animal.species.name)
        self.feeding_deque.push_back(f"{icon} {animal.name}")
        self._update_feed_list()
        self._update_buttons_state()

    def _add_to_feeding_urgent(self):
        """deque - добавление в начало очереди (срочное кормление)."""
        idx = self.animals_list.currentRow()
        animals = list(self.farm)
        if idx < 0 or idx >= len(animals):
            return

        animal = animals[idx]
        icon = get_animal_icon(animal.species.name)
        self.feeding_deque.push_front(f"🚨 {icon} {animal.name}")
        self._update_feed_list()
        self._update_buttons_state()

    def _update_feed_list(self):
        """Обновление отображения очереди."""
        self.feed_list.clear()
        temp = []
        while not self.feeding_deque.is_empty():
            temp.append(self.feeding_deque.pop_front())
        for i, item in enumerate(temp):
            prefix = "➡️" if i == 0 else "⏳"
            self.feed_list.addItem(f"{prefix} {item}")
            self.feeding_deque.push_back(item)
        self._update_buttons_state()

    def _feed_next(self):
        """Кормление следующего из очереди."""
        if self.feeding_deque.is_empty():
            return

        animal = self.feeding_deque.pop_front()
        self._update_feed_list()
        self._update_buttons_state()

        self.feed_progress.setFormat(f"Кормим {animal}...")
        self.feed_progress.setValue(0)

        self.timer = QTimer()
        self.timer.timeout.connect(lambda: self._animate_feeding(animal))
        self.timer.start(30)

    def _animate_feeding(self, animal):
        """Анимация прогресс-бара."""
        value = self.feed_progress.value() + 2
        self.feed_progress.setValue(value)

        if value >= 100:
            self.timer.stop()
            self.feed_progress.setFormat("✓ Готов!")
            self.feed_progress.setValue(0)
            self.feed_progress.setFormat("Готов к кормлению")
