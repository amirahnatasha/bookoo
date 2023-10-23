# bookoo - A book tracker website

This website is called 'bookoo', a pun from the Malay word 'buku,' which reads the same as 'bookoo' and means 'book.' 'Bookoo' is a web application designed to help users organize and manage their personal book collections, join book clubs, and engage in meaningful discussions about literature.

## Features

- **User Registration and Authentication**: Users can create accounts, log in, and securely manage their book collections and club memberships.

- **Bookshelf Management**: Users can add books to their bookshelves by searching for books using the Open Library database. Book details such as title, author, cover image, and description are automatically retrieved.

- **Note-taking**: Users can add personal notes and comments to individual books in their bookshelves, enhancing their reading experience and keeping track of important information.

- **Book Clubs**: Users can create and join book clubs, fostering a sense of community among readers who share common interests.

- **Discussion Forums**: Book club members can participate in discussion forums dedicated to their chosen books, facilitating lively and insightful conversations.


## Distinctiveness and Complexity

- **API Integration**: The website leverages the Open Library API to seamlessly integrate book data into user bookshelves. This integration ensures up-to-date book information, including cover images and descriptions.

- **User-Generated Content**: The ability for users to add personal notes and comments to their books adds a layer of interactivity and customization to their bookshelves.

- **Community Building**: The creation of book clubs and discussion forums encourages users to connect with fellow book enthusiasts, fostering a sense of community around a shared love for literature.

- **Intuitive User Experience**: Efforts have been made to design a user interface that is easy to navigate, ensuring that users can effortlessly manage their book collections and engage with the community.

## Files Overview

### Important Files

- **`views.py`**: This file contains functions for adding, removing, and managing books, bookshelves, clubs, and discussions.

- **`models.py`**: This file includes models for users, books, bookshelves, clubs, posts, and more. 

- **`urls.py`**: This file contains all the  URLs configuration.

- **`templates/`**: This directory contains HTML templates used to render the web pages, including the main layout, bookshelfs, and book club pages.

- **`static/`**: This static files directory to store static assets like CSS stylesheets and JavaScript files.

## Getting Started

To run the Bookoo application locally:

1. Clone the repository.
2. Create a virtual environment and install the required dependencies from `requirements.txt`.
3. Configure your database settings in `settings.py`.
4. Run migrations to create the database schema.
5. Start the development server using `python manage.py runserver`.

You can access the application in your web browser at `http://localhost:8000/`.

[![IMAGE ALT TEXT]([http://img.youtube.com/vi/PGHTFmwBrNI/0.jpg)](https://youtu.be/PGHTFmwBrNI "Bookoo Website")


