import os
import django
from django.db.models import QuerySet, F
from decimal import Decimal


# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models here
from main_app.models import Pet
from main_app.models import Artifact
from main_app.models import Location
from main_app.models import Car
from main_app.models import Task
from main_app.models import HotelRoom
from main_app.choices import RoomTypeChoice
from main_app.models import Character
from main_app.choices import ClassTypeChoice

# Run and print your queries

def create_pet(name: str, species: str):
    Pet.objects.create(
        name=name,
        species=species
    )
    return f"{name} is a very cute {species}!"


def create_artifact(name: str, origin: str, age: int, description: str, is_magical: bool):
    Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical
    )

    return f"The artifact {name} is {age} years old!"


def rename_artifact(artifact: Artifact, new_name: str):
    if artifact.is_magical and artifact.age > 250:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts():
    Artifact.objects.all().delete()


def show_all_locations() -> str:
    locations = Location.objects.all().order_by('-id')

    return '\n'.join(f"{l.name} has a population of {l.population}!" for l in locations)


def new_capital() -> None:
    # Location.objects.first().update(is_capital=True)

    location = Location.objects.first()
    location.is_capital = True
    location.save()


def get_capitals() -> QuerySet[dict]:
    return Location.objects.filter(is_capital=True).values('name')

def delete_first_location() -> None:
    Location.objects.first().delete()


def apply_discount():
    cars = Car.objects.all()


    for car in cars:
        percentage_off = Decimal(str(sum(int(digit) for digit in str(car.year)) / 100))
        discount = car.price * percentage_off
        car.price_with_discount = car.price - discount
        car.save()


def get_recent_cars():
    return Car.objects.filter(year__gt=2020).values('model', 'price')


def delete_last_car():
    Car.objects.last().delete()


def show_unfinished_tasks():
    unfinished_tasks = Task.objects.filter(is_finished=False)

    return '\n'.join(f"Task - {u.title} needs to be done until {u.due_date}!" for u in unfinished_tasks)


def complete_odd_tasks():
    all_tasks = Task.objects.all()

    for task in all_tasks:
        if task.id % 2 == 1:
            task.is_finished = True
            task.save()


def encode_and_replace(text: str, task_title: str):
    encoded_text = ''.join(chr(ord(c) - 3) for c in text)

    for t in Task.objects.filter(title=task_title):
        t.description = encoded_text
        t.save()


def get_deluxe_rooms():
    deluxe_rooms = HotelRoom.objects.filter(room_type=RoomTypeChoice.DELUXE)

    return '\n'.join(f"Deluxe room with number {r.room_number} costs {r.price_per_night}$ per night!" for r in deluxe_rooms if r.id % 2 == 0)



def increase_room_capacity():
    rooms = HotelRoom.objects.all().order_by('id')
    previous_room: HotelRoom = None

    for room in rooms:
        if not room.is_reserved:
            continue

        if previous_room:
            room.capacity += previous_room.capacity

        else:
            room.capacity += room.id

        previous_room = room
        room.save()


def reserve_first_room():
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()

def delete_last_room():
    last_room = HotelRoom.objects.last()

    if not last_room.is_reserved:
        last_room.delete()


def update_characters():
    Character.objects.filter(class_name=ClassTypeChoice.MAGE).update(
        level=F('level') + 3,
        intelligence=F('intelligence') - 7,
    )

    Character.objects.filter(class_name=ClassTypeChoice.WARRIOR).update(
        hit_points=F('hit_points') / 2,
        dexterity=F('dexterity') + 4,
    )

    Character.objects.filter(class_name__in=[ClassTypeChoice.ASSASSIN, ClassTypeChoice.SCOUT]).update(
        inventory='The inventory is empty'
    )


def fuse_characters(first_character: Character, second_character: Character) -> None:
    fusion_inventory = None

    if first_character.class_name in [ClassTypeChoice.MAGE, ClassTypeChoice.SCOUT]:
        fusion_inventory = 'Bow of the Elven Lords, Amulet of Eternal Wisdom'
    else:
        fusion_inventory = 'Dragon Scale Armor, Excalibur'

    Character.objects.create(
        name=first_character.name + ' ' + second_character.name,
        class_name=ClassTypeChoice.FUSION,
        level=(first_character.level + second_character.level) // 2,
        strength=(first_character.strength + second_character.strength) * 1.2,
        dexterity=(first_character.dexterity + second_character.dexterity) * 1.4,
        intelligence=(first_character.intelligence + second_character.intelligence) * 1.5,
        hit_points=first_character.hit_points + second_character.hit_points,
        inventory=fusion_inventory,
    )
    first_character.delete()
    second_character.delete()


def grand_dexterity():
    Character.objects.update(dexterity=30)


def grand_intelligence():
    Character.objects.update(intelligence=40)


def grand_strength():
    Character.objects.update(strength=50)


def delete_characters():
    Character.objects.filter(inventory='The inventory is empty').delete()
