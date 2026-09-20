"""Small in-memory backend for the Aryan Retail librarian demo."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Book:
    """A book title that can have one copy checked out at a time."""

    title: str
    author: str
    available: bool = True
    borrowed_by: str | None = None

    def summary(self) -> dict[str, str | bool | None]:
        return {
            "title": self.title,
            "author": self.author,
            "available": self.available,
            "borrowed_by": self.borrowed_by,
        }


class LibraryCatalog:
    """A session-scoped, mock catalog for renting and receiving books."""

    def __init__(self) -> None:
        self._books = {
            "the hobbit": Book("The Hobbit", "J. R. R. Tolkien"),
            "pride and prejudice": Book("Pride and Prejudice", "Jane Austen"),
            "dune": Book("Dune", "Frank Herbert"),
            "a brief history of time": Book(
                "A Brief History of Time", "Stephen Hawking"
            ),
        }

    def search(self, query: str) -> list[dict[str, str | bool | None]]:
        """Find titles or authors matching a spoken query."""
        normalized_query = query.casefold().strip()
        return [
            book.summary()
            for book in self._books.values()
            if normalized_query in book.title.casefold()
            or normalized_query in book.author.casefold()
        ]

    def rent(self, title: str, member_name: str) -> dict[str, str | bool | None]:
        """Check out an available title to a named member."""
        book = self._find_exact(title)
        if book is None:
            return {"success": False, "message": f"I could not find {title}."}
        if not book.available:
            return {
                "success": False,
                "message": f"{book.title} is currently rented by {book.borrowed_by}.",
            }

        book.available = False
        book.borrowed_by = member_name.strip()
        return {
            "success": True,
            "title": book.title,
            "member_name": book.borrowed_by,
            "message": f"{book.title} has been rented to {book.borrowed_by}.",
        }

    def receive(self, title: str) -> dict[str, str | bool | None]:
        """Receive a previously rented title back into the library."""
        book = self._find_exact(title)
        if book is None:
            return {"success": False, "message": f"I could not find {title}."}
        if book.available:
            return {"success": False, "message": f"{book.title} is already checked in."}

        returned_by = book.borrowed_by
        book.available = True
        book.borrowed_by = None
        return {
            "success": True,
            "title": book.title,
            "member_name": returned_by,
            "message": f"{book.title} has been received and is now available.",
        }

    def loans_for(self, member_name: str) -> list[dict[str, str | bool | None]]:
        """List all titles currently rented by one member."""
        normalized_name = member_name.casefold().strip()
        return [
            book.summary()
            for book in self._books.values()
            if book.borrowed_by and book.borrowed_by.casefold() == normalized_name
        ]

    def _find_exact(self, title: str) -> Book | None:
        return self._books.get(title.casefold().strip())
