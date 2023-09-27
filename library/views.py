from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from itertools import chain
from django.contrib import messages

from .models import User, Book, Read, TBR, CR, Club, Genre, Post, Note

def index(request):
    books = Book.objects.all()
    return render(request, "library/index.html", {
        "books" : books
    })

def bookClub(request):
    clubs = Club.objects.all()

    return render(request, "library/bookclub.html", {
        "clubs" : clubs,
    })

def bookInfo(request, book_id):

    user = request.user

    book = Book.objects.get(pk=book_id)
    
    new_image = book.image.replace('-S.jpg', '-L.jpg')

    description = book.description
    
    strings_to_remove = ['([source', '[Source']

    for string in strings_to_remove:
        if string in description:
            description = description.split(string)[0].strip()

    notes = Note.objects.filter(author=user, book=book)

    return render(request, "library/book_info.html", {
        "book" : book,
        "image" : new_image,
        "description" : description,
        "notes" : notes
    })

def newNotes(request, book_id):
    if request.method == "POST":
        user = request.user
        book = Book.objects.get(pk=book_id)
        notes = request.POST["notes"]

        newNotes = Note(
            book = book,
            author = user,
            notes = notes
        )

        newNotes.save()

    return HttpResponseRedirect(reverse(bookInfo, args=[book_id]))

def newPost(request, club_id):
    if request.method == "POST":
        user = request.user
        club = Club.objects.get(pk=club_id)
        post = request.POST["post"]

        newPost = Post(
            posted_by = user,
            club = club,
            post = post,
            likes = 0
        )

        newPost.save()

    return HttpResponseRedirect(reverse(clubPage, args=[club_id]))

def clubForm(request):
    user = request.user

    genres = Genre.objects.all()
    cr = CR.objects.filter(user=user)
    read = Read.objects.filter(user=user)
    tbr = TBR.objects.filter(user=user)

    all_books  = chain(cr, read, tbr)

    # Check if the user is already a member of any club
    user_joined = Club.objects.filter(members=user).exists()

    # Check if the user created a club
    user_create_club = Club.objects.filter(created_by=user).exists()

    return render(request, "library/club_form.html", {
        "genres" : genres,
        "cr" : all_books,
        "user_joined": user_joined,
        "created" : user_create_club
    })

def newClub(request):
    if request.method == "POST":

        user = request.user

        name = request.POST["name"]
        description = request.POST["description"]
        image = request.POST["image"]
        genre = request.POST["genre"]
        max = request.POST["max"]
        current_read = request.POST["current_read"]

        if not image:
            image = "https://www.colleges-fenway.org/wp-content/uploads/2022/09/bookclub.jpeg"

        genreData = Genre.objects.get(genre=genre)

        # print("Current Read Title:", current_read)
        # current_read_cr = Book.objects.get(title=current_read)

        try:
            current_read_cr = Book.objects.get(title=current_read)
        except Book.DoesNotExist:
            current_read_cr = None
        except Book.MultipleObjectsReturned:
            # Handle the case where there are multiple books with the same title
            # You can choose which one to use or handle it as needed
            current_read_cr = Book.objects.filter(title=current_read).first()
        
        newClub = Club(
            name = name,
            description = description,
            image = image,
            max = max,
            genre = genreData,
            current_read = current_read_cr,
            created_by = user
        )

        newClub.save()

        # Add creator as member of the club
        newClub.members.add(user)

        return HttpResponseRedirect(reverse(bookClub))


def clubPage(request, club_id):
    user = request.user
    club = Club.objects.get(pk=club_id)
    members = club.members.all()

    # Check if user is a member in the club
    user_joined = club.members.filter(id=user.id).exists()

    user_joined_other = user.clubs_joined.exists()

    all_posts = Post.objects.filter(club=club).order_by('-timestamp')

    p = Paginator(all_posts, 10)
    page = request.GET.get('page', 1)
    posts = p.get_page(page)

    return render(request, "library/club_page.html",{
        "club" : club,
        "members" : members,
        "posts" : posts,
        "user_joined" : user_joined,
        "user_joined_other" : user_joined_other
    })

def joinClub(request, club_id):
    club_to_join = Club.objects.get(pk=club_id)
    user = request.user

    # Check if the user is already a member of the club
    is_member = club_to_join.members.filter(id=user.id).exists()

    if is_member:
        error_message = "You are already a member of this club."
    elif club_to_join.created_by == user:
        error_message = "You can't join a club you created."
    else:
        club_to_join.members.add(user)
        club_to_join.save()
        return HttpResponseRedirect(reverse(clubPage, args=[club_id]))

    return render(request, 'library/club_page.html', {
        'club': club_to_join, 
        'message': error_message
    })

def leaveClub(request, club_id):
    
    user = request.user

    club = Club.objects.get(pk=club_id)

    if user in club.members.all():
        club.members.remove(user)
        messages.success(request, f"You have left {club.name}.")
    else:
        messages.error(request, "You are not a member of this club.")

    return HttpResponseRedirect(reverse(clubPage, args=[club_id]))

def addBookRead(request):
    if request.method == 'POST':
        
        user= request.user

        data = json.loads(request.body)
        isbn = data["isbn"]
        author = data["author"]
        title = data["title"]
        pages = data["pages"]
        description = data["description"]
        image = data["image"]

        # Check if a book with the same ISBN already exists
        if Read.objects.filter(user=user, book__isbn=isbn).exists():
            return JsonResponse({'message': 'Book already exists in your Read bookshelf.'}, status=400)
        
        print("Received Description:", description)

        book = Book(
            isbn=isbn,
            title=title,
            author=author,
            pages=pages,
            description=description,
            image=image
        )
        book.save()

        #Save book in read
        read = Read(
            user= user,
            book = book
        )
        read.save()

        message = title + ' added successfully in Read.'

        return JsonResponse({'message': message})

    return JsonResponse({'message': 'Invalid request'})

def addBookTBR(request):
    if request.method == 'POST':
        
        user= request.user

        data = json.loads(request.body)
        isbn = data["isbn"]
        author = data["author"]
        title = data["title"]
        pages = data["pages"]
        description = data["description"]
        image = data["image"]

        # Check if a book with the same ISBN already exists
        if TBR.objects.filter(user=user, book__isbn=isbn).exists():
            return JsonResponse({'message': 'Book already exists in your TBR bookshelf.'}, status=400)

        book = Book(
            isbn=isbn,
            title=title,
            author=author,
            pages=pages,
            description=description,
            image=image
        )
        book.save()

        #Save book in tbr
        tbr = TBR(
            user= user,
            book = book
        )
        tbr.save()

        message = title + ' added successfully in TBR.'

        return JsonResponse({'message': message})

    return JsonResponse({'message': 'Invalid request'})

def addBookCR(request):
    if request.method == 'POST':
        
        user= request.user

        data = json.loads(request.body)
        isbn = data["isbn"]
        author = data["author"]
        title = data["title"]
        pages = data["pages"]
        description = data["description"]
        image = data["image"]

        # Check if a book with the same ISBN already exists
        if CR.objects.filter(user=user, book__isbn=isbn).exists():
            return JsonResponse({'message': 'Book already exists in your Current Read.'}, status=400)

        book = Book(
            isbn=isbn,
            title=title,
            author=author,
            pages=pages,
            description=description,
            image=image
        )
        book.save()

        #Save book in cr
        cr = CR(
            user= user,
            book = book
        )
        cr.save()

        message = title + ' added successfully in Current Read.'

        return JsonResponse({'message': message})

    return JsonResponse({'message': 'Invalid request'})

def removeBook(request, book_id):
    
    book = Book.objects.get(pk=book_id)
    book.delete()

    return JsonResponse({"message" : "Book removed."})

def bookshelf(request):
    user = request.user
    books = Read.objects.filter(user=user)
    return render(request, "library/bookshelf.html", {
        "books" : books,
        "title" : "Read"
    })

def tbr(request):
    user = request.user
    books = TBR.objects.filter(user=user)
    return render(request, "library/bookshelf.html", {
        "books" : books,
        "title" : "TBR"
    })

def cr(request):
    user = request.user
    books = CR.objects.filter(user=user)
    return render(request, "library/bookshelf.html", {
        "books" : books,
        "title" : "Current Read"
    })

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "library/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "library/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "library/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "library/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "library/register.html")