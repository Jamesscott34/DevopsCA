from django.test import TestCase
from .models import Book
from datetime import datetime
from django.contrib.auth.hashers import check_password
from .models import User
from .models import Tag, Notification

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
            published_date=datetime.strptime("01-01-2023", "%d-%m-%Y").date(),
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
        from django.db import IntegrityError, transaction

        Book.objects.create(
            title="Book One",
            author="Author One",
            description="First book with unique ISBN.",
            published_date=datetime.strptime("01-01-2023", "%d-%m-%Y").date(),
            isbn="js1111111111"
        )
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Book.objects.create(
                    title="Book Two",
                    author="Author Two",
                    description="Second book with duplicate ISBN.",
                    published_date=datetime.strptime("02-01-2023", "%d-%m-%Y").date(),
                    isbn="js1111111111"
                )

    def test_required_fields(self):
        """
        Test that missing required fields raise an error.
        """
        from django.db import IntegrityError, transaction
        # Missing title
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Book.objects.create(
                    title=None,
                    author="Author",
                    description="Missing title.",
                    published_date=datetime.strptime("01-01-2023", "%d-%m-%Y").date(),
                    isbn="js2222222222"
                )
        # Missing author
        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                Book.objects.create(
                    title="Title",
                    author=None,
                    description="Missing author.",
                    published_date=datetime.strptime("01-01-2023", "%d-%m-%Y").date(),
                    isbn="js3333333333"
                )

    def test_increment_view_count(self):
        """
        Test that the increment_view_count method increases the view count.

        This test creates a Book, calls increment_view_count, and checks that
        the view_count field is incremented as expected.
        """
        book = Book.objects.create(
            title="View Count Book",
            author="View Author",
            description="Testing view count increment.",
            published_date=datetime.strptime("01-01-2023", "%d-%m-%Y").date(),
            isbn="js4444444444"
        )
        self.assertEqual(book.view_count, 0)
        book.increment_view_count()
        book.refresh_from_db()
        self.assertEqual(book.view_count, 1)
        book.increment_view_count()
        book.refresh_from_db()
        self.assertEqual(book.view_count, 2)

    def test_get_most_read_and_most_viewed(self):
        """
        Test the get_most_read and get_most_viewed class methods.

        This test creates several books with varying read and view counts,
        then checks that the methods return the correct books in order.
        """
        # Create books with different read and view counts
        b1 = Book.objects.create(
            title="Book 1",
            author="Author 1",
            description="Book 1 description.",
            published_date=datetime.strptime("01-01-2023", "%d-%m-%Y").date(),
            isbn="js5555555551",
            is_read=True,
            view_count=5
        )
        b2 = Book.objects.create(
            title="Book 2",
            author="Author 2",
            description="Book 2 description.",
            published_date=datetime.strptime("02-01-2023", "%d-%m-%Y").date(),
            isbn="js5555555552",
            is_read=True,
            view_count=10
        )
        b3 = Book.objects.create(
            title="Book 3",
            author="Author 3",
            description="Book 3 description.",
            published_date=datetime.strptime("03-01-2023", "%d-%m-%Y").date(),
            isbn="js5555555553",
            is_read=False,
            view_count=20
        )

        most_read = list(Book.get_most_read())
        most_viewed = list(Book.get_most_viewed())

        self.assertEqual(most_read[0], b2)
        self.assertEqual(most_read[1], b1)
        self.assertNotIn(b3, most_read)  # b3 is not marked as read

        self.assertEqual(most_viewed[0], b3)
        self.assertEqual(most_viewed[1], b2)
        self.assertEqual(most_viewed[2], b1)

    def test_assign_tags_to_book(self):
        """
        Test that tags can be assigned to a book and retrieved.

        This test creates tags, assigns them to a book, and verifies the assignment.
        """
        tag1 = Tag.objects.create(name="Fiction")
        tag2 = Tag.objects.create(name="Science")
        book = Book.objects.create(
            title="Tagged Book",
            author="Tag Author",
            description="Book with tags.",
            published_date=datetime.strptime("04-01-2023", "%d-%m-%Y").date(),
            isbn="js6666666666"
        )
        book.tags.add(tag1, tag2)
        self.assertEqual(book.tags.count(), 2)
        self.assertIn(tag1, book.tags.all())
        self.assertIn(tag2, book.tags.all())

    def test_book_str_representation(self):
        """
        Test the string representation of a Book.

        This test creates a book and checks that its string representation is its title.
        """
        book = Book.objects.create(
            title="String Book",
            author="String Author",
            description="Book for __str__ test.",
            published_date=datetime.strptime("05-01-2023", "%d-%m-%Y").date(),
            isbn="js7777777777"
        )
        self.assertEqual(str(book), "String Book")

class UserModelTest(TestCase):
    """
    Test suite for the User model in the Book Catalog application.
    """

    def test_user_authentication(self):
        """
        Test that a user can be authenticated with the correct password.

        This test creates a user, checks that the password is hashed,
        and verifies authentication using Django's check_password.
        """
        raw_password = "mysecretpassword"
        user = User.objects.create(
            username="testuser",
            email="testuser@example.com",
            password=raw_password
        )
        self.assertNotEqual(user.password, raw_password)  # Should be hashed
        self.assertTrue(check_password(raw_password, user.password))

    def test_notification_creation_and_mark_as_read(self):
        """
        Test creating a notification for a user and marking it as read.

        This test creates a user and a notification, then marks it as read and checks the status.
        """
        user = User.objects.create(
            username="notifuser",
            email="notifuser@example.com",
            password="notifpass"
        )
        notification = Notification.objects.create(
            user=user,
            title="Test Notification",
            message="This is a test notification.",
            notification_type="general"
        )
        self.assertFalse(notification.is_read)
        notification.mark_as_read()
        notification.refresh_from_db()
        self.assertTrue(notification.is_read)
