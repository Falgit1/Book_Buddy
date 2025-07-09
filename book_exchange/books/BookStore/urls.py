from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('<int:book_id>/', views.book_detail, name='book_detail'),
    path('<int:book_id>/request_phone_number/', views.request_phone_number, name='request_phone_number'),
    path('sell/', views.sell_book, name='sell_book'),
    path('user_books/', views.user_books, name='user_books'),
    path('view_cart/', views.view_cart, name='view_cart'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
]
