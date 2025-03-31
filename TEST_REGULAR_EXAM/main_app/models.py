from django.core.validators import MinLengthValidator, MaxLengthValidator, MinValueValidator, MaxValueValidator
from django.db import models
from main_app.managers import CustomerManager


# Create your models here.
class Publisher(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3),
            MaxLengthValidator(100)
        ]
    )
    established_date = models.DateField(default='1800-01-01')
    country = models.CharField(
        max_length=40,
        validators=[
            MaxLengthValidator(40)
        ],
        default='TBC'
    )
    rating = models.FloatField(
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(5.0)
        ],
        default=0.0
    )
    objects = CustomerManager()


class Author(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[
            MinLengthValidator(3),
            MaxLengthValidator(100)
        ]
    )
    birth_date = models.DateField(blank=True, null=True)
    country = models.CharField(
        max_length=40,
        validators=[
            MaxLengthValidator(40)
        ],
        default='TBC'
    )
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)


class Book(models.Model):
    GENRE_CHOICES = [
        ('Fiction', 'Fiction'),
        ('Non-Fiction', 'Non-Fiction'),
        ('Other', 'Other'),
    ]


    title = models.CharField(
        max_length=200,
        validators=[
            MinLengthValidator(2),
            MaxLengthValidator(200)
        ]
    )
    publication_date = models.DateField()
    summary = models.TextField(blank=True, null=True)
    genre = models.CharField(
        max_length=11,
        choices=GENRE_CHOICES,
        validators=[
            MaxLengthValidator(11)
        ],
        default='Other'
    )
    price = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[
            MinValueValidator(0.01),
            MaxValueValidator(9999.99)
        ],
        default=0.01
    )
    rating = models.FloatField(
        validators=[
            MinValueValidator(0.0),
            MaxValueValidator(5.0)
        ],
        default=0.0
    )
    is_bestseller = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)
    publisher = models.ForeignKey(
        to=Publisher,
        on_delete=models.CASCADE
    )
    main_author = models.ForeignKey(
        to=Author,
        on_delete=models.CASCADE,
        related_name='main_books'
    )
    co_authors = models.ManyToManyField(
        to=Author,
        related_name='co_authored_books'
    )
