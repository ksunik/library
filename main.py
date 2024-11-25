"""
main.py

Автор: ksunik
Дата: 2023-11-24
Описание: Основная программа, которая выполняет управление библиотекой.
"""


import json
from typing import Dict, List, Optional

from exceptions import InvalidBookDataError, FileSaveError


class LibraryManager:
    def __init__(self, name_file: str = "library.json") -> None:
        self.name_file:  str = name_file
        self.library: Dict[int, Dict[str, str]] = self.load_info_from_file()

    def load_info_from_file(self) -> Dict[int, Dict[str, str]]:
        """Загружает данные из файла."""
        try:
            with open(self.name_file, "r") as file:
                raw_data = json.load(file)
                return {int(key): value for key, value in raw_data.items()}
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def save_info_to_file(self) -> bool:
        """Сохраняет данные в файл."""
        try:
            with open(self.name_file, "w") as file:
                json.dump(self.library, file, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            raise FileSaveError(f"Ошибка при сохранении данных в файл: {e}")

    def add_book(self, title: str, author: str, year: str) -> Dict[str, str]:
        """Добавляет новую книгу в библиотеку."""
        if not title and not author and not year:
            raise InvalidBookDataError(
                "Название, автор и год книги не могут быть пустыми."
                )

        try:
            book_id: int = int(max(self.library.keys(), default=0)) + 1
            book: Dict[str, str] = {
                "title": title,
                "author": author,
                "year": year,
                "status": "в наличии",
            }
            self.library[book_id] = book
            try:
                self.save_info_to_file()
            except FileSaveError as e:
                raise FileSaveError(
                    f"Ошибка при сохранении данных в файл: {e}"
                    )
            return {**book, "id": book_id}
        except Exception as e:
            raise Exception(f"Ошибка при добавлении книги: {e}")

    def delete_book(self, book_id: int) -> Optional[Dict[str, str]]:
        """Удаляет книгу из библиотеки."""
        if book_id in self.library:
            deleted_book: Dict[str, str] = self.library.pop(book_id)
            try:
                self.save_info_to_file()
            except FileSaveError as e:
                raise FileSaveError(
                    f"Ошибка при сохранении данных в файл: {e}"
                    )
            return deleted_book
        else:
            return None

    def search_books(self, search_field: str) -> List[Dict[str, str]]:
        """Поиск книги в библиотеке."""
        results: List[Dict[str, str]] = []
        search_field_lower: str = search_field.lower()

        for book_id, book in self.library.items():
            if (
                search_field_lower in book['title'].lower() or
                search_field_lower in book['author'].lower() or
                search_field_lower in book['year'].lower()
            ):
                results.append({**book, "id": book_id})
        return results

    def show_all_books(self) -> List[Dict[str, str]]:
        """Показывает все книги в библиотеке."""
        return [
            {**book, "id": book_id} for book_id, book in self.library.items()
        ]

    def change_book_status(self, book_id: int, status: str) -> bool:
        """Изменяет статус книги."""
        if status not in ["в наличии", "выдана"]:
            return False
        if book_id in self.library:
            self.library[book_id]["status"] = status
            try:
                self.save_info_to_file()
            except FileSaveError as e:
                raise FileSaveError(
                    f"Ошибка при сохранении данных в файл: {e}"
                    )
            return True
        else:
            return False

    def get_book_id(self, book: Dict[str, str]) -> Optional[int]:
        """Возвращает ID книги (вспомогательная функция)."""
        for book_id, b in self.library.items():
            if b == book:
                return book_id
        return None


def main() -> None:
    library: LibraryManager = LibraryManager()

    while True:
        print(
            "\nМеню:\n"
            "1. Добавить книгу\n"
            "2. Удалить книгу\n"
            "3. Найти книгу\n"
            "4. Показать все книги\n"
            "5. Изменить статус книги\n"
            "6. Выйти"
        )

        choice: str = input("Для выбора действия напечатайте цифру: ")

        if choice == "1":
            title: str = input("Введите название книги: ")
            author: str = input("Введите автора книги: ")
            year: str = input("Введите год издания книги: ")
            try:
                added_book: Dict[str, str] = library.add_book(
                    title, author, year
                    )
                if added_book:
                    print(
                        f"Книга '{added_book['title']}' "
                        f"({added_book['author']}, {added_book['year']}) "
                        f"успешно добавлена с ID {added_book['id']}."
                        )
                else:
                    print("Ошибка: не удалось добавить книгу.")
            except InvalidBookDataError as e:
                print(f"Ошибка: {e}")
        elif choice == "2":
            try:
                book_id: int = int(input("Введите ID книги для удаления: "))
                deleted_book: Optional[
                    Dict[str, str]
                    ] = library.delete_book(book_id)
                if deleted_book:
                    print(f"Книга '{deleted_book['title']}' успешно удалена.")
                else:
                    print(f"Книга с ID {book_id} не найдена.")
            except ValueError:
                print("ID должен быть числом.")
        elif choice == "3":
            search_field: str = input("Введите значение для поиска: ")
            found_books: List[Dict[str, str]] = library.search_books(
                search_field
                )
            if found_books:
                print("Найденные книги:")
                for book in found_books:
                    print(
                        f"ID: {book['id']}, Название: {book['title']}, "
                        f"Автор: {book['author']}, Год: {book['year']}, "
                        f"Статус: {book['status']}"
                    )
            else:
                print("Ничего не найдено.")
        elif choice == "4":
            all_books: List[Dict[str, str]] = library.show_all_books()
            if all_books:
                print("Все книги в библиотеке:")
                for book in all_books:
                    print(
                        f"ID: {book['id']}, Название: {book['title']}, "
                        f"Автор: {book['author']}, Год: {book['year']}, "
                        f"Статус: {book['status']}"
                    )
            else:
                print("Библиотека пуста.")
        elif choice == "5":
            try:
                book_id: int = int(input(
                    "Введите ID книги для изменения статуса: "
                    ))
                status: str = input(
                    "Введите новый статус ('в наличии' или 'выдана'): "
                    )
                if library.change_book_status(book_id, status):
                    print(
                        f"Статус книги с ID {book_id} успешно изменён "
                        f"на '{status}'.")
                else:
                    print(
                        "Не удалось изменить статус. Проверьте ID книги или "
                        "корректность статуса."
                    )
            except ValueError:
                print("ID должен быть числом.")
        elif choice == "6":
            print("Выход из программы. До свидания!")
            break
        else:
            print("Некорректный выбор. Попробуйте снова.")


if __name__ == "__main__":
    main()
