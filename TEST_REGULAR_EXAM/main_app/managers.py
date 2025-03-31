from django.db import models
from django.db.models import Count


class CustomerManager(models.Manager):
    def get_publishers_by_books_count(self):
        return self.annotate(book_count=Count('book')).order_by('-book_count', 'name')
