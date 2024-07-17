from django.urls import path
from .import views

urlpatterns = [
    path('api/book/list/', views.book_list, name = 'book-list'),
    path('api/book/details/<int:id>/', views.book_details, name = 'book-details'),


    #author api
    path('api/author/create/', views.author_register_view, name = 'author-list'),
    path('api/author/list/', views.author_list_view, name = 'author-list'),

    path('api/author/login/', views.author_login_view, name = 'author-login'),
    path('api/author/profile/', views.author_profile, name = 'author-profile'),

    path("api/author/reset/password/", views.author_password_reset_view, name = 'author-password-reset')
]
