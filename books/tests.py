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
            published_date="2023-01-01",
            isbn="1234567890123"
        )
        retrieved = Book.objects.get(isbn="1234567890123")
        self.assertEqual(retrieved.title, "Test Book")
        self.assertEqual(retrieved.author, "Test Author")
