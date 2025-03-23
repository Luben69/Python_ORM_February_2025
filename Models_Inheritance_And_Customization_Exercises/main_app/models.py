from enum import StrEnum

from django.core.exceptions import ValidationError
from django.db import models
from datetime import date, timedelta
from django.db.models import QuerySet


# Create your models here.
class BaseCharacter(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    class Meta:
        abstract = True


class Mage(BaseCharacter):
    elemental_power = models.CharField(max_length=100)
    spellbook_type = models.CharField(max_length=100)


class Assassin(BaseCharacter):
    weapon_type = models.CharField(max_length=100)
    assassination_technique = models.CharField(max_length=100)


class DemonHunter(BaseCharacter):
    weapon_type = models.CharField(max_length=100)
    demon_slaying_ability = models.CharField(max_length=100)


class TimeMage(Mage):
    time_magic_mastery = models.CharField(max_length=100)
    temporal_shift_ability = models.CharField(max_length=100)


class Necromancer(Mage):
    raise_dead_ability = models.CharField(max_length=100)


class ViperAssassin(Assassin):
    venomous_strikes_mastery = models.CharField(max_length=100)
    venomous_bite_ability = models.CharField(max_length=100)


class ShadowbladeAssassin(Assassin):
    shadowstep_ability = models.CharField(max_length=100)


class VengeanceDemonHunter(DemonHunter):
    vengeance_mastery = models.CharField(max_length=100)
    retribution_ability = models.CharField(max_length=100)


class FelbladeDemonHunter(DemonHunter):
    felblade_ability = models.CharField(max_length=100)


class UserProfile(models.Model):
    username = models.CharField(max_length=70, unique=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)


class Message(models.Model):
    sender = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    receiver = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
        related_name='received_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)


    def mark_as_read(self):
        self.is_read = True


    def reply_to_message(self, reply_content: str):
        new_message = Message(
            sender=self.receiver,
            receiver=self.sender,
            content=reply_content
        )
        new_message.save()

        return new_message


    def forward_message(self, receiver: UserProfile):
        forwarded_message = Message(
            sender=self.receiver,
            receiver=receiver,
            content=self.content
        )
        forwarded_message.save()

        return forwarded_message


class StudentIDField(models.PositiveIntegerField):
    @staticmethod
    def validate_field(value) -> int:
        try:
            return int(value)
        except ValueError:
            raise ValueError('Invalid input for student ID')


    def to_python(self, value):
        return self.validate_field(value)

    def get_prep_value(self, value):
        validated_value = self.validate_field(value)

        if validated_value <= 0:
            raise ValidationError('ID cannot be less than or equal to zero')

        return validated_value


class Student(models.Model):
    name = models.CharField(max_length=100)
    student_id = StudentIDField()


class MaskedCreditCardField(models.CharField):
    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = 19
        super().__init__(*args, **kwargs)

    @staticmethod
    def validate_card_number(value):
        if not isinstance(value, str):
            raise ValidationError("The card number must be a string")

        if not value.isdigit():
            raise ValidationError("The card number must contain only digits")

        if len(value) != 16:
            raise ValidationError("The card number must be exactly 16 characters long")

        return value

    def to_python(self, value):
        value = self.validate_card_number(value)
        return f"****-****-****-{value[-4:]}"

    def get_prep_value(self, value):
        return self.to_python(value)


class CreditCard(models.Model):
    card_owner = models.CharField(max_length=100)
    card_number = MaskedCreditCardField()


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)


class Room(models.Model):
    hotel = models.ForeignKey(
        Hotel,
        on_delete= models.CASCADE
    )
    number = models.CharField(max_length=100, unique=True)
    capacity = models.PositiveIntegerField()
    total_guests = models.PositiveIntegerField()
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)

    def clean(self):
        if self.total_guests > self.capacity:
            raise ValidationError('Total guests are more than the capacity of the room')


    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        return f"Room {self.number} created successfully"

class ReservationType(StrEnum):
    REGULAR = 'Regular'
    SPECIAL = 'Special'


class BaseReservation(models.Model):
    class Meta:
        abstract = True

    reservation_type = None

    room = models.ForeignKey(
        to=Room,
        on_delete= models.CASCADE
    )
    start_date = models.DateField()
    end_date = models.DateField()


    def reservation_period(self):
        return (self.end_date - self.start_date).days


    def calculate_total_cost(self):
        return round(self.room.price_per_night * self.reservation_period(), 2)


    def get_overlapping_reservations(self, start_date: date, end_date: date) -> QuerySet['BaseReservation']:
        return self.__class__.objects.filter(
            room=self.room,
            end_date__gte=start_date,
            start_date__lte=end_date
        )


    @property
    def is_available(self):
        reservations = self.get_overlapping_reservations(self.start_date, self.end_date)
        return not reservations.exists


    def clean(self):
        if self.start_date >= self.end_date:
            raise ValidationError('Start date cannot be after or in the same end date')

        if not self.is_available:
            return f"Room {self.room.number} cannot be reserved"

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
        return f"{self.reservation_type} reservation for room {self.room.number}"


class RegularReservation(BaseReservation):
    reservation_type = ReservationType.REGULAR.value


class SpecialReservation(BaseReservation):
    reservation_type = ReservationType.SPECIAL.value

    def extend_reservation(self, days: int):
        new_end_date = self.end_date + timedelta(days=days)
        reservations = self.get_overlapping_reservations(self.start_date, new_end_date)

        if reservations:
            raise ValidationError("Error during extending reservation")

        self.end_date = new_end_date
        self.save()

        return f"Extended reservation for room {self.room.number} with {days} days"
