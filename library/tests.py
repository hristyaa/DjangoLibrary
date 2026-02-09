from django.test import TestCase
from .models import Author, Book

# Create your tests here.


class ModelTests(TestCase):
    def setUp(self):
        self.author = Author.objects.create(first_name='John', last_name='Doe')
        self.book = Book.objects.create(
            title='Test Book',
            author=self.author,
        )

    def test_author_str(self):
        self.assertEqual(str(self.author), 'John')

    def test_book_str(self):
        self.assertEqual(str(self.book), 'Test Book')

    def test_book_author_relationship(self):
        self.assertEqual(self.book.author, self.author)
        self.assertEqual(self.author.book.first(), self.book)
