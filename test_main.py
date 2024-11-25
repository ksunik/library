"""
test_main.py

Автор: ksunik
Дата: 2023-11-24
Описание: Тестирование функций из main.py.
"""


import unittest
from main import LibraryManager
import os


class TestLibraryManager(unittest.TestCase):
    def setUp(self) -> None:
        """Создаём временный файл для тестирования."""
        self.test_file = "test_library.json"
        self.manager = LibraryManager(self.test_file)

    def tearDown(self) -> None:
        """Удаляем временный файл после тестирования."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_add_book(self):
        """Проверка добавления книги."""
        book = self.manager.add_book(
            "Преступление и наказание", "Ф. Достоевский", "1866"
            )
        self.assertIsNotNone(book)
        self.assertEqual(book["title"], "Преступление и наказание")
        self.assertEqual(book["author"], "Ф. Достоевский")
        self.assertEqual(book["year"], "1866")
        self.assertIn(book["id"], self.manager.library)

    def test_delete_book(self):
        """Проверка удаления книги."""
        book = self.manager.add_book("Война и мир", "Л. Толстой", "1869")
        self.assertIn(book["id"], self.manager.library)
        deleted_book = self.manager.delete_book(book["id"])
        self.assertIsNotNone(deleted_book)
        self.assertEqual(deleted_book["title"], "Война и мир")
        self.assertNotIn(book["id"], self.manager.library)

    def test_search_books(self):
        """Проверка поиска книг."""
        self.manager.add_book(
            "Преступление и наказание", "Ф. Достоевский", "1866"
            )
        self.manager.add_book("Братья Карамазовы", "Ф. Достоевский", "1880")
        results = self.manager.search_books("Достоевский")
        self.assertEqual(len(results), 2)
        titles = [book["title"] for book in results]
        self.assertIn("Преступление и наказание", titles)
        self.assertIn("Братья Карамазовы", titles)

    def test_show_all_books(self):
        """Проверка отображения всех книг."""
        self.manager.add_book(
            "Преступление и наказание", "Ф. Достоевский", "1866"
            )
        self.manager.add_book("Братья Карамазовы", "Ф. Достоевский", "1880")
        all_books = self.manager.show_all_books()
        self.assertEqual(len(all_books), 2)
        ids = [book["id"] for book in all_books]
        self.assertIn(1, ids)
        self.assertIn(2, ids)

    def test_change_book_status(self):
        """Проверка изменения статуса книги."""
        book = self.manager.add_book(
            "Преступление и наказание", "Ф. Достоевский", "1866"
            )
        success = self.manager.change_book_status(book["id"], "выдана")
        self.assertTrue(success)
        self.assertEqual(self.manager.library[book["id"]]["status"], "выдана")
        failure = self.manager.change_book_status(book["id"], "недоступно")
        self.assertFalse(failure)

    def test_load_and_save(self):
        """Проверка загрузки и сохранения данных."""
        self.manager.add_book(
            "Преступление и наказание", "Ф. Достоевский", "1866"
            )
        self.manager.save_info_to_file()

        new_manager = LibraryManager(self.test_file)
        self.assertEqual(len(new_manager.library), 1)
        book = new_manager.library[1]
        self.assertEqual(book["title"], "Преступление и наказание")
        self.assertEqual(book["author"], "Ф. Достоевский")
        self.assertEqual(book["year"], "1866")

    def test_get_book_id(self):
        """Проверка получения ID книги."""
        added_book = self.manager.add_book(
            "Преступление и наказание", "Ф. Достоевский", "1866"
            )
        book = {
            "title": added_book["title"],
            "author": added_book["author"],
            "year": added_book["year"],
            "status": added_book["status"],
        }
        book_id = self.manager.get_book_id(book)
        self.assertEqual(book_id, 1)


if __name__ == "__main__":
    unittest.main()
