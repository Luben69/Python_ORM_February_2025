import os
import django
from django.db.models import Q, F, Count, Avg

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here

# Create queries within functions
# caller.py
from datetime import date
from main_app.models import Publisher, Author, Book


def populate_db():
    # Create Publishers
    publisher_1 = Publisher.objects.create(
        name="Oxford Press",
        established_date=date(1800, 1, 1),
        country="UK",
        rating=4.8
    )
    publisher_2 = Publisher.objects.create(
        name="Penguin Books",
        established_date=date(1935, 1, 1),
        country="USA",
        rating=4.7
    )

    # Create Authors
    author_1 = Author.objects.create(
        name="J.K. Rowling",
        birth_date=date(1965, 7, 31),
        country="UK",
        is_active=True
    )
    author_2 = Author.objects.create(
        name="George Orwell",
        birth_date=date(1903, 6, 25),
        country="India",
        is_active=False
    )

    # Create Books
    book_1 = Book.objects.create(
        title="Harry Potter and the Sorcerer's Stone",
        publication_date=date(1997, 6, 26),
        summary="A young wizard embarks on magical adventures at Hogwarts.",
        genre="Fiction",
        price=19.99,
        rating=4.9,
        is_bestseller=True,
        publisher=publisher_1,
        main_author=author_1
    )
    book_2 = Book.objects.create(
        title="1984",
        publication_date=date(1949, 6, 8),
        summary="A dystopian novel about totalitarianism and surveillance.",
        genre="Fiction",
        price=14.99,
        rating=4.8,
        is_bestseller=False,
        publisher=publisher_2,
        main_author=author_2
    )

    # Adding co-authors to the books (optional)
    book_1.co_authors.add(author_2)  # For example, add George Orwell as co-author for Harry Potter

    # Optionally, print success message or return any response
    print("Database populated successfully!")


def get_publishers(search_string=None):
    # Check if no search criteria
    if search_string is None:
        return "No search criteria."

    # Check for empty string criteria
    if search_string == "":
        return "No search criteria."

    # Filter publishers based on the search string
    publishers = Publisher.objects.filter(
        Q(name__icontains=search_string) | Q(country__icontains=search_string)
    ).order_by('-rating', 'name')

    # If no publishers match
    if not publishers:
        return "No publishers found."

    # Create the output string
    result = []
    for publisher in publishers:
        # Format the country and rating
        country_display = 'Unknown' if publisher.country == 'TBC' else publisher.country
        rating_display = f"{publisher.rating:.1f}"

        result.append(f"Publisher: {publisher.name}, country: {country_display}, rating: {rating_display}")

    # Join all results with newline
    return "\n".join(result)


def get_top_publisher():
    # Retrieve the publisher with the greatest number of books
    publishers = Publisher.objects.annotate(num_of_books=Count('book')).order_by('-num_of_books', 'name')

    # If there are no publishers, return "No publishers found."
    if not publishers:
        return "No publishers found."

    # Get the top publisher (first one after sorting)
    top_publisher = publishers.first()

    # Format the result string
    return f"Top Publisher: {top_publisher.name} with {top_publisher.num_of_books} books."


def get_top_main_author():
    # Retrieve authors and their count of main books, ordered by count (descending), then by name (ascending)
    authors = Author.objects.annotate(num_books=Count('main_books')).order_by('-num_books', 'name')

    # If no authors or no books exist, return "No results."
    if not authors or not Book.objects.exists():
        return "No results."

    # Get the author with the most main books (first in the list after sorting)
    top_author = authors.first()

    # Retrieve the titles of the books that the author is the main author of
    book_titles = top_author.main_books.all().order_by('title')
    book_titles_list = [book.title for book in book_titles]

    # Calculate the average rating of these books
    avg_rating = book_titles.aggregate(Avg('rating'))['rating__avg']

    # Format the rating to one decimal place
    if avg_rating is None:
        avg_rating = 0.0  # In case there are no ratings available for the books.

    avg_rating = round(avg_rating, 1)

    # Format the book titles as a comma-separated string
    book_titles_str = ", ".join(book_titles_list)

    # Return the formatted string
    return f"Top Author: {top_author.name}, own book titles: {book_titles_str}, books average rating: {avg_rating}"


def get_authors_by_books_count():
    # Annotate each author with the total number of books they have (main books + co-authored books)
    authors = Author.objects.annotate(num_books=Count('main_books') + Count('co_authored_books'))

    # Order authors by the total number of books (descending), and by name (ascending)
    authors = authors.order_by('-num_books', 'name')

    # Check if there are any authors to return
    if not authors.exists() or all(author.num_books == 0 for author in authors):
        return "No results."

    # Format the top 3 authors as required, or all authors if there are fewer than 3
    result = []
    for author in authors[:3]:
        result.append(f"{author.name} authored {author.num_books} books.")

    return "\n".join(result)


def get_top_bestseller():
    # Retrieve bestsellers and order by rating (descending), and title (ascending) in case of a tie
    books = Book.objects.filter(is_bestseller=True).order_by('-rating', 'title')

    # Check if there are any bestsellers
    if not books:
        return "No results."

    # Get the top book (first one in the sorted list)
    top_book = books.first()

    # Get the main author and co-authors
    main_author = top_book.main_author.name
    co_authors = top_book.co_authors.all()

    # Format co-authors' names, if any, otherwise 'N/A'
    if co_authors:
        co_author_names = sorted(co_authors.values_list('name', flat=True))
        co_authors_str = ", ".join(co_author_names)
    else:
        co_authors_str = "N/A"

    # Format the book rating to the first decimal place
    rating = f"{top_book.rating:.1f}"

    # Return the formatted string
    return f"Top bestseller: {top_book.title}, rating: {rating}. Main author: {main_author}. Co-authors: {co_authors_str}."


def increase_price():
    # Get all books published in 2025 with a rating >= 4.0
    books_to_update = Book.objects.filter(
        publication_date__year=2025,
        rating__gte=4.0
    )

    # If no books match the criteria, return "No changes in price."
    if not books_to_update.exists():
        return "No changes in price."

    # Update the price for each book by 20%
    books_to_update.update(price=F('price') * 1.20)

    # Return the formatted string with the number of books updated
    return f"Prices increased for {books_to_update.count()} books."
