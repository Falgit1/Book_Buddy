from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='book_images/', null=True, blank=True)
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class PhoneNumberRequest(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    viewer = models.ForeignKey(User, on_delete=models.CASCADE)
    request_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Phone number requested for {self.book.title} by {self.viewer.username}"
