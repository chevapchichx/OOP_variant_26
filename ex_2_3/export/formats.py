"""Паттерн Мост (BRIDGE) - форматы импорта/экспорта

Проблема:
Есть данные (животные) и способы хранения (JSON, CSV, TXT).
При прямом подходе нужны разные классы для каждого формата.

Решение:
Абстракция ExportFormat и конкретные реализации (JSON, CSV, TXT).
Данные содержат ссылку на формат - это "мост" между абстракцией и реализацией.
"""

import json
import csv
from abc import ABC, abstractmethod


# Реализация - интерфейс формата
class ExportFormat(ABC):
    """Абстрактный формат экспорта - Implementation в паттерне Мост."""

    @abstractmethod
    def export(self, data, filepath):
        pass

    @abstractmethod
    def import_data(self, filepath):
        pass

    @abstractmethod
    def get_extension(self):
        pass

    @abstractmethod
    def get_name(self):
        pass


# Конкретные реализации форматов
class JsonFormat(ExportFormat):
    """JSON - универсальный текстовый формат."""

    def export(self, data, filepath):
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            return False

    def import_data(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return []

    def get_extension(self):
        return ".json"

    def get_name(self):
        return "JSON"


class CsvFormat(ExportFormat):
    """CSV - табличный формат, совместим с Excel."""

    def export(self, data, filepath):
        try:
            if not data:
                return False
            with open(filepath, 'w', encoding='utf-8', newline='') as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
            return True
        except Exception:
            return False

    def import_data(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                result = []
                for row in reader:
                    # Стандартизация ключей: название полей может быть разным
                    normalized = {}
                    for key, value in row.items():
                        key_lower = key.strip().lower()
                        if key_lower in ('name', 'имя'):
                            normalized['name'] = value
                        elif key_lower in ('species', 'вид'):
                            normalized['species'] = value
                        elif key_lower in ('genus', 'род'):
                            normalized['genus'] = value
                        elif key_lower in ('family', 'семейство'):
                            normalized['family'] = value
                        elif key_lower in ('order', 'отряд'):
                            normalized['order'] = value
                        elif key_lower in ('class', 'класс'):
                            normalized['class'] = value
                        elif key_lower in ('phylum', 'тип'):
                            normalized['phylum'] = value
                        elif key_lower in ('age', 'возраст'):
                            normalized['age'] = int(value) if value else 0
                        elif key_lower in ('weight', 'вес'):
                            normalized['weight'] = float(
                                value) if value else 0.0
                        elif key_lower in ('description', 'описание'):
                            normalized['description'] = value
                    if normalized.get('name') and normalized.get('species'):
                        result.append(normalized)
                return result
        except Exception:
            return []

    def get_extension(self):
        return ".csv"

    def get_name(self):
        return "CSV"


class TxtFormat(ExportFormat):
    """TXT - простой текстовый формат."""

    def export(self, data, filepath):
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                for item in data:
                    line = ";".join(str(v) for v in item.values())
                    f.write(line + "\n")
            return True
        except Exception:
            return False

    def import_data(self, filepath):
        try:
            result = []
            with open(filepath, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue

                    # Обработка формата: name;species;genus;family;order;class;phylum;age;weight
                    parts = line.split(';')
                    if len(parts) >= 7:
                        try:
                            item = {
                                'name': parts[0].strip(),
                                'species': parts[1].strip(),
                                'genus': parts[2].strip(),
                                'family': parts[3].strip(),
                                'order': parts[4].strip(),
                                'class': parts[5].strip(),
                                'phylum': parts[6].strip(),
                                'age': int(parts[7]) if len(parts) > 7 and parts[7].strip() else 0,
                                'weight': float(parts[8]) if len(parts) > 8 and parts[8].strip() else 0.0,
                                'description': parts[9].strip() if len(parts) > 9 else ''
                            }
                            if item['name'] and item['species']:
                                result.append(item)
                        except (ValueError, IndexError):
                            continue
            return result
        except Exception:
            return []

    def get_extension(self):
        return ".txt"

    def get_name(self):
        return "TXT"
