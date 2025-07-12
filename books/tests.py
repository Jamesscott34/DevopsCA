from django.test import TestCase
from .models import Book

# Create your tests here.

class BookModelTest(TestCase):
    """
    Test suite for the Book model in the Book Catalog application.

    This class contains unit tests to verify the correct behavior of the Book model,
    including creation, retrieval, and field validation.
    """

    def test_create_and_retrieve_book(self):
        """
        Test that a Book can be created and retrieved from the database.

        This test creates a Book instance with sample data, saves it to the database,
        and then retrieves it by its ISBN to verify that the stored data matches
        the input values.
        """
        book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            description="A test book for unit testing.",
            published_date="2023-01-01",
            isbn="js1234567890"
        )
        retrieved = Book.objects.get(isbn="js1234567890")
        self.assertEqual(retrieved.title, "Test Book")
        self.assertEqual(retrieved.author, "Test Author")
        self.assertEqual(retrieved.description, "A test book for unit testing.")

    def test_unique_isbn_constraint(self):
        """
        Test that the Book model enforces unique ISBN values.

        This test creates a Book with a specific ISBN, then attempts to create
        another Book with the same ISBN. It should raise an IntegrityError.
        """
        from django.db import IntegrityError

        Book.objects.create(
            title="Book One",
            author="Author One",
            description="First book with unique ISBN.",
            published_date="2023-01-01",
            isbn="js1111111111"
        )
        with self.assertRaises(IntegrityError):
            Book.objects.create(
                title="Book Two",
                author="Author Two",
                description="Second book with duplicate ISBN.",
                published_date="2023-01-02",
                isbn="js1111111111"
            )
