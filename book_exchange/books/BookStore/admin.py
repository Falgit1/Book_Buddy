from django.contrib import admin

# Register your models here.
from .models import Book,PhoneNumberRequest

admin.site.register(Book)
admin.site.register(PhoneNumberRequest)