from django.test import TestCase
from .models import Author, Book

# Create your tests here.


class ModelTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(
            first_name="John",
            last_name="Doe",
            birth_date="1799-01-10",
        )
        self.book = Book.objects.create(
            title="Test Book",
            publication_date='1833-01-01',
            author=self.author,
        )

    def test_author_str(self):
        self.assertEqual(str(self.author), "John Doe")

    def test_book_str(self):
        self.assertEqual(str(self.book), "Test Book")
