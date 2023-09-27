from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addBookRead", views.addBookRead, name="addBookRead"),
    path("addBookTBR", views.addBookTBR, name="addBookTBR"),
    path("addBookCR", views.addBookCR, name="addBookCR"),
    path("bookshelf", views.bookshelf, name="bookshelf"),
    path("tbr", views.tbr, name="tbr"),
    path("cr", views.cr, name="cr"),
    path("book/<int:book_id>", views.bookInfo, name="book_info"),
    path("removeBook/<int:book_id>", views.removeBook, name="removeBook"),
    path("bookClub", views.bookClub, name="bookClub"),
    path("clubForm", views.clubForm, name="club_form"),
    path("newClub", views.newClub, name="new_club"),
    path("club/<int:club_id>", views.clubPage, name="club_page"),
    path("joinClub/<int:club_id>", views.joinClub, name="join_club"),
    path("leaveClub/<int:club_id>", views.leaveClub, name="leave_club"),
    path("club/<int:club_id>/newPost", views.newPost, name="new_post"),
    path("book/<int:book_id>/newNotes", views.newNotes, name="new_note")
    
]