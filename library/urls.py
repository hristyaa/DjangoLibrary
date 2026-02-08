from django.urls import path, include
# from .views import book_detail, books_list
from .views import *

app_name = 'library'

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('students/', include('students.urls', namespace='students'))
# ]

urlpatterns = [
    path('authors/', AuthorListView.as_view(), name='authors_list'),
    path('author/new/', AuthorCreateView.as_view(), name='author_create'),
    path('author/update/<int:pk>/', AuthorUpdateView.as_view(), name='author_update'),

    path('books/', BooksListView.as_view(), name='books_list'),
    path('books/new/', BookCreateView.as_view(), name='book_create'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
    path('books/update/<int:pk>/', BookUpdateView.as_view(), name='book_update'),
    path('books/delete/<int:pk>/', BookDeleteView.as_view(), name='book_delete'),
    path('books/recommend/<int:pk>/', RecommendBookView.as_view(), name='book_recommend'),
    path('books/review/<int:pk>/', ReviewBookView.as_view(), name='book_review'),
    # path('books_list/', books_list, name='books_list'),
    # path('book_detail/<int:book_id>', book_detail, name='book_detail'),
]
