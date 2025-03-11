import os
from typing import List

import django
from django.db.models import Case, When, Value

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

# Import your models
from main_app.models import ArtworkGallery
from main_app.models import Laptop
from main_app.choices import OperationSystemChoices
from main_app.models import ChessPlayer
from main_app.models import Meal
from main_app.choices import MealTypeChoices
from main_app.models import Dungeon
from main_app.choices import DungeonDifficultyChoices
from main_app.models import Workout
from main_app.choices import WorkOutTypeChoices

# Create and check models
# Run and print your queries


def show_highest_rated_art():
    highest_rated = ArtworkGallery.objects.order_by('-rating', 'id').first()

    return f"{highest_rated.art_name} is the highest-rated art with a {highest_rated.rating} rating!"


def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery) -> None:
    ArtworkGallery.objects.bulk_create([
        first_art,
        second_art,
    ])


def delete_negative_rated_arts():
    ArtworkGallery.objects.filter(rating__lt=0).delete()


def show_the_most_expensive_laptop():
    the_laptop = Laptop.objects.order_by('-price', '-id').first()
    return f"{the_laptop.brand} is the most expensive laptop available for {the_laptop.price}$!"


def bulk_create_laptops(args: List[Laptop]) -> None:
    Laptop.objects.bulk_create(args)


def update_to_512_GB_storage():
    Laptop.objects.filter(brand__in=['Asus', 'Lenovo']).update(storage=512)


def update_to_16_GB_memory():
    Laptop.objects.filter(brand__in=['Apple', 'Dell', 'Acer']).update(memory=16)


def update_operation_systems():
    Laptop.objects.update(
        operation_system=Case(
            When(brand='Asus', then=Value(OperationSystemChoices.WINDOWS)),
            When(brand='Apple', then=Value(OperationSystemChoices.MACOS)),
            When(brand__in=['Dell', 'Acer'], then=Value(OperationSystemChoices.LINUX)),
            When(brand='Lenovo', then=Value(OperationSystemChoices.CHROME_OS)),
        )
    )


def delete_inexpensive_laptops():
    Laptop.objects.filter(price__lt=1200).delete()


def bulk_create_chess_players(args: List[ChessPlayer]):
    ChessPlayer.objects.bulk_create(args)


def delete_chess_players():
    ChessPlayer.objects.filter(title='no title').delete()


def change_chess_games_won():
    ChessPlayer.objects.filter(title='GM').update(games_won=30)


def change_chess_games_lost():
    ChessPlayer.objects.filter(title='no title').update(games_lost=25)


def change_chess_games_drawn():
    ChessPlayer.objects.all().update(games_drawn=10)


def grand_chess_title_GM():
    ChessPlayer.objects.filter(rating__gte=2400).update(title='GM')


def grand_chess_title_IM():
    ChessPlayer.objects.filter(
        rating__lte=2399,
        rating__gte=2300
    ).update(title='IM')


def grand_chess_title_FM():
    ChessPlayer.objects.filter(
        rating__lte=2299,
        rating__gte=2200
    ).update(title='FM')


def grand_chess_title_regular_player():
    ChessPlayer.objects.filter(
        rating__lte=2199,
        rating__gte=0
    ).update(title='regular player')


def set_new_chefs():
    Meal.objects.filter(meal_type=MealTypeChoices.BREAKFAST).update(chef='Gordon Ramsay')
    Meal.objects.filter(meal_type=MealTypeChoices.LUNCH).update(chef='Julia Child')
    Meal.objects.filter(meal_type=MealTypeChoices.DINNER).update(chef='Jamie Oliver')
    Meal.objects.filter(meal_type=MealTypeChoices.SNACK).update(chef='Thomas Keller')


def set_new_preparation_times():
    Meal.objects.filter(meal_type=MealTypeChoices.BREAKFAST).update(preparation_time='10 minutes')
    Meal.objects.filter(meal_type=MealTypeChoices.LUNCH).update(preparation_time='12 minutes')
    Meal.objects.filter(meal_type=MealTypeChoices.DINNER).update(preparation_time='15 minutes')
    Meal.objects.filter(meal_type=MealTypeChoices.SNACK).update(preparation_time='5 minutes')


def update_low_calorie_meals():
    Meal.objects.filter(
        meal_type__in=[MealTypeChoices.BREAKFAST,MealTypeChoices.DINNER]).update(calories=400)


def update_high_calorie_meals():
    Meal.objects.filter(
        meal_type__in=[MealTypeChoices.LUNCH, MealTypeChoices.SNACK]).update(calories=700)


def delete_lunch_and_snack_meals():
    Meal.objects.filter(
        meal_type__in=[MealTypeChoices.LUNCH, MealTypeChoices.SNACK]).delete()


def show_hard_dungeons():
    hard_ordered_dungeons = Dungeon.objects.filter(
        difficulty=DungeonDifficultyChoices.HARD
    ).order_by('-location')

    return '\n'.join(f"{h.name} is guarded by {h.boss_name} who has {h.boss_health} health points!"
                     for h in hard_ordered_dungeons)


def bulk_create_dungeons(args: List[Dungeon]) -> None:
    Dungeon.objects.bulk_create(args)


def update_dungeon_names():
    Dungeon.objects.update(
        name=Case(
            When(difficulty=DungeonDifficultyChoices.EASY, then=Value('The Erased Thombs')),
            When(difficulty=DungeonDifficultyChoices.MEDIUM, then=Value('The Coral Labyrinth')),
            When(difficulty=DungeonDifficultyChoices.HARD, then=Value('The Lost Haunt')),
        )
    )


def update_dungeon_bosses_health():
    Dungeon.objects.exclude(difficulty=DungeonDifficultyChoices.EASY).update(boss_health=500)


def update_dungeon_recommended_levels():
    Dungeon.objects.update(
        recommended_level=Case(
            When(difficulty=DungeonDifficultyChoices.EASY, then=Value(25)),
            When(difficulty=DungeonDifficultyChoices.MEDIUM, then=Value(50)),
            When(difficulty=DungeonDifficultyChoices.HARD, then=Value(75)),
        )
    )


def update_dungeon_rewards() -> None:
    Dungeon.objects.filter(boss_health=500).update(reward='1000 Gold')
    Dungeon.objects.filter(location__startswith='E').update(reward='New dungeon unlocked')
    Dungeon.objects.filter(location__endswith='s').update(reward='Dragonheart Amulet')


def set_new_locations() -> None:
    Dungeon.objects.filter(recommended_level=25).update(location='Enchanted Maze')
    Dungeon.objects.filter(recommended_level=50).update(location='Grimstone Mines')
    Dungeon.objects.filter(recommended_level=75).update(location='Shadowed Abyss')


def show_workouts():
    they_types_wanted = Workout.objects.filter(
        workout_type__in=[WorkOutTypeChoices.CALISTHENICS, WorkOutTypeChoices.CROSSFIT]
    ).order_by('id')

    return '\n'.join(f"{t.name} from {t.workout_type} type has {t.difficulty} difficulty!"
                     for t in they_types_wanted)


def get_high_difficulty_cardio_workouts():
    return Workout.objects.filter(
        workout_type=WorkOutTypeChoices.CARDIO,
        difficulty='High'
    ).order_by('instructor')


def set_new_instructors():
    Workout.objects.update(
        instructor=Case(
            When(workout_type=WorkOutTypeChoices.CARDIO, then=Value('John Smith')),
            When(workout_type=WorkOutTypeChoices.STRENGTH, then=Value('Michael Williams')),
            When(workout_type=WorkOutTypeChoices.YOGA, then=Value('Emily Johnson')),
            When(workout_type=WorkOutTypeChoices.CROSSFIT, then=Value('Sarah Davis')),
            When(workout_type=WorkOutTypeChoices.CALISTHENICS, then=Value('Chris Heria')),
        )
    )


def set_new_duration_times():
    Workout.objects.update(
        duration=Case(
            When(instructor='John Smith', then=Value('15 minutes')),
            When(instructor='Sarah Davis', then=Value('30 minutes')),
            When(instructor='Chris Heria', then=Value('45 minutes')),
            When(instructor='Michael Williams', then=Value('1 hour')),
            When(instructor='Emily Johnson', then=Value('1 hour and 30 minutes')),
        )
    )


def delete_workouts():
    Workout.objects.exclude(
        workout_type__in=[WorkOutTypeChoices.STRENGTH, WorkOutTypeChoices.CALISTHENICS]
    ).delete()
