from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Book(models.Model):
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    pages = models.IntegerField(default='0000000')
    description = models.CharField(max_length=100000)
    image = models.CharField(max_length=100)
    isbn = models.CharField(max_length=250, default='0000000')

    def __str__(self):
        return '{} by {}'.format(self.title, self.author)

class Read(models.Model):
    user = models .ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_read")
    book = models .ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True, related_name="book_read")

    def __str__(self):
        return '{} read {}'.format(self.user, self.book)
    
class TBR(models.Model):
    user = models .ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_tbr")
    book = models .ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True, related_name="book_tbr")

    def __str__(self):
        return '{} wants to read {}'.format(self.user, self.book)
    
class CR(models.Model):
    user = models .ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="user_cr")
    book = models .ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True, related_name="book_cr")

    def __str__(self):
        return '{} is currently reading {}'.format(self.user, self.book)
    
class Genre(models.Model):
    genre = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.genre)
    
class Club(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="club_creator")
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=250)
    description = models.CharField(max_length=1000)
    current_read = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True, related_name="club_cr")
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE, blank=True, null=True, related_name="club_genre")
    max = models.IntegerField(default=1)
    members = models.ManyToManyField(User, related_name="clubs_joined")

    def __str__(self):
        return '{} created {} book club'.format(self.created_by, self.name)
    
class Post(models.Model):
    post = models.CharField(max_length=500)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="posted_by")
    club = models.ForeignKey(Club, on_delete=models.CASCADE, blank=True, null=True, related_name="club_posts")
    timestamp = models.DateTimeField(auto_now_add=True)
    likes = models.IntegerField(default=0)

    def __str__(self):
        return '{} created a post'.format(self.posted_by)
    
class Like(models.Model):
    post_liked = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True, related_name="post_liked")
    liked_by = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="liked_by")

    def __str__(self):
        return '{} liked {}'.format(self.liked_by, self.post_liked)
    
class Note(models.Model):
    notes = models.CharField(max_length=50000)
    book = models .ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=True, related_name="book_notes")
    author = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, related_name="notes_author")