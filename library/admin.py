from django.contrib import admin
from .models import User, Book, Read, CR, TBR, Genre, Club, Post, Note

# Register your models here.
admin.site.register(User)
admin.site.register(Book)
admin.site.register(Read)
admin.site.register(Genre)
admin.site.register(Club)
admin.site.register(CR)
admin.site.register(TBR)
admin.site.register(Post)
admin.site.register(Note)