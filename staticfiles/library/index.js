
function getCookie(name){
    const value = `; ${name}=`;
    const parts = value.split(`; ${name}=`);
    if(parts.length == 2) return parts.pop().split(';').shift();
}

function getBooks() {
    document.getElementById("output").innerHTML = "";

    const query = document.getElementById("input").value;

    fetch("http://openlibrary.org/search.json?q=" + query)
    .then(response => response.json())
    .then(data => {
        const books = data.docs.slice(0, 10);

        books.forEach(book => {
            const isbn = book.isbn[0];
            const title = book.title;
            const author = book.author_name[0];
            const pages = book.number_of_pages_median;
            const key = book.key;

            const dropdown =
                '<div class="dropdown"><button class="btn btn-drop dropdown-toggle" type="button" data-bs-toggle="dropdown" aria-expanded="false">Add to bookshelf</button><ul class="dropdown-menu">';

            const read = (
                '<li><a class="dropdown-item add-book-read" data-isbn="' + isbn + '" data-title="' + title + '" data-author="' + author + '" data-pages="' + pages + '" data-key="' + key + '">Read</a></li>'
            );

            const tbr =(
                '<li><a class="dropdown-item add-book-tbr" data-isbn="' + isbn + '" data-title="' + title + '" data-author="' + author + '" data-pages="' + pages + '" data-key="' + key + '">TBR</a></li>'
            );

            const cr =(
                '<li><a class="dropdown-item add-book-cr" data-isbn="' + isbn + '" data-title="' + title + '" data-author="' + author + '" data-pages="' + pages + '" data-key="' + key + '">CR</a></li></ul></div>'
            );

            const bookContainer = document.createElement("div");
            bookContainer.className = 'book-container';
            bookContainer.dataset.isbn = isbn;
            const url = "/library/book"; // Hard code url
        
            bookContainer.innerHTML = `
                <img src="http://covers.openlibrary.org/b/isbn/${isbn}-S.jpg" alt="${title}" class="book-image">
                <div class="book-info">
                        <p class="book-title book-info" data-isbn="${isbn}" data-title="${title}" data-author="${author}" data-pages="${pages}" data-key="${key}">${title}</p>
                    <p class="book-author">${author}</p>
                    ${isAuthenticated ? dropdown + read + tbr + cr : ''}
                </div>
            `;


            document.getElementById("output").appendChild(bookContainer);
        });

        attachEventListeners();
    });
}


function attachEventListeners() {
    var buttons = document.getElementsByClassName('add-book-read');
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].removeEventListener('click', addBookRead); 
        buttons[i].addEventListener('click', addBookRead);
    }

    var buttons = document.getElementsByClassName('add-book-tbr');
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].removeEventListener('click', addBookTBR); 
        buttons[i].addEventListener('click', addBookTBR);
    }

    var buttons = document.getElementsByClassName('add-book-cr');
    for (var i = 0; i < buttons.length; i++) {
        buttons[i].removeEventListener('click', addBookCR); 
        buttons[i].addEventListener('click', addBookCR);
    }

}

function getBookInfo(event) {
    event.preventDefault();
    var isbn = this.dataset.isbn;
    var title = this.dataset.title;
    var author = this.dataset.author;
    var pages = this.dataset.pages;
    var key = this.dataset.key;
    var image = "http://covers.openlibrary.org/b/isbn/" + isbn + "-S.jpg";

    var description = "";

    // Get book description
    fetch(`https://openlibrary.org${key}.json`)
    .then( a => a.json())
    .then(response => {
        description = response.description;

        // Create a JSON object with book data
        var bookData = {
            isbn: isbn,
            title: title,
            author: author,
            pages: pages,
            description: description,
            image: image
        };

        // Send a POST request to view
        fetch(`/library/bookInfo`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').getAttribute('value')
            },
            body: JSON.stringify(bookData)
        })
        .then(response => response.json())
        .then(result => {
            // Handle the response from the server if needed
        });
    })

    return isbn, title, author, pages, key, image, description
}

function addBookRead(event) {
    event.preventDefault();
    
    var isbn = this.dataset.isbn;
    var title = this.dataset.title;
    var author = this.dataset.author;
    var pages = this.dataset.pages;
    var key = this.dataset.key;
    var image = "http://covers.openlibrary.org/b/isbn/" + isbn + "-S.jpg";

    fetch(`https://openlibrary.org${key}.json`)
    .then( a => a.json())
    .then(response => {
        var description = response.description;

        // console.log("desc" + description);

        fetch(`/library/addBookRead`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').getAttribute('value')
            },
            body: JSON.stringify({
                isbn : isbn,
                title : title,
                author : author,
                pages : pages,
                description : description,
                image : image
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            const message = document.querySelector("#message");
            message.innerHTML = result.message;

            message.style.display = 'block';

            setTimeout(() => {
                message.style.opacity = '0';
                setTimeout(() => {
                    message.style.display = 'none';
                    message.style.opacity = '1';
                }, 1000);
            }, 3000);
        })
    })

}

function addBookTBR(event) {
    // event.preventDefault();
    var isbn = this.dataset.isbn;
    var title = this.dataset.title;
    var author = this.dataset.author;
    var pages = this.dataset.pages;
    var key = this.dataset.key;
    var image = "http://covers.openlibrary.org/b/isbn/" + isbn + "-S.jpg";

    // Get book description
    fetch(`https://openlibrary.org${key}.json`)
    .then( a => a.json())
    .then(response => {
        var description = response.description;

        fetch(`/library/addBookTBR`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').getAttribute('value')
            },
            body: JSON.stringify({
                isbn : isbn,
                title : title,
                author : author,
                pages : pages,
                description : description,
                image : image
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            const message = document.querySelector("#message");
            message.innerHTML = result.message;

            message.style.display = 'block';

            setTimeout(() => {
                message.style.opacity = '0';
                setTimeout(() => {
                    message.style.display = 'none';
                    message.style.opacity = '1';
                }, 1000);
            }, 3000);
        })
    })

    
}

function addBookCR(event) {
    event.preventDefault();
    
    var isbn = this.dataset.isbn;
    var title = this.dataset.title;
    var author = this.dataset.author;
    var pages = this.dataset.pages;
    var key = this.dataset.key;
    var image = "http://covers.openlibrary.org/b/isbn/" + isbn + "-S.jpg";

    // Get book description
    fetch(`https://openlibrary.org${key}.json`)
    .then( a => a.json())
    .then(response => {
        var description = response.description;

        fetch(`/library/addBookCR`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('input[name="csrfmiddlewaretoken"]').getAttribute('value')
            },
            body: JSON.stringify({
                isbn : isbn,
                title : title,
                author : author,
                pages : pages,
                description : description,
                image : image
            })
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            const message = document.querySelector("#message");
            message.innerHTML = result.message;

            message.style.display = 'block';

            setTimeout(() => {
                message.style.opacity = '0';
                setTimeout(() => {
                    message.style.display = 'none';
                    message.style.opacity = '1';
                }, 1000);
            }, 3000);
        })
    })

}

function remove(book_id){
    
    fetch(`/library/removeBook/${book_id}`)
    .then(response => response.json())
    .then(result => {
        console.log(result);

        const message = document.querySelector("#message");
        message.innerHTML = result.message;

        message.style.display = 'block';

        setTimeout(() => {
            message.style.opacity = '0';
            setTimeout(() => {
                message.style.display = 'none';
                message.style.opacity = '1';
            }, 1000);
            location.reload()
        }, 3000);

        })

}