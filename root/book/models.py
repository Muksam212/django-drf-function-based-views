from django.db import models

from root.utils import BaseModel

from django.contrib.auth.models import User
# Create your models here.

class Author(BaseModel):
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "authors")

    def __str__(self):
        return f"{self.user.username}"
    

class Book(BaseModel):
    author = models.ForeignKey(Author, on_delete = models.CASCADE, related_name = "author_book")
    pdf = models.FileField(upload_to = 'book/pdf', null = True, blank = False)
    title = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.title}"