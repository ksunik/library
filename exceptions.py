"""
exceptions.py

Автор: ksunik
Дата: 2023-11-24
Описание: Исключения для проекта.
"""


class FileSaveError(Exception):
    """Ошибка при сохранении данных в файл."""
    pass


class InvalidBookDataError(Exception):
    """Ошибка при добавлении книги с некорректными данными."""
    pass
