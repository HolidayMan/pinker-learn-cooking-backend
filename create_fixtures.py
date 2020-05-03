import os
import json

# generating categories

counter = 1
choices = {
    'drinks': "Напитки",
    'first_courses': "Первые блюда",
    'salads': "Салаты",
    'sandwiches': "Бутеры",
    'second_courses': "Вторые блюда"
}

categories_folders_names = sorted(['images/main/' + photo for photo in os.listdir('media/images/main')])

categories = []
for choice, photo_path in zip(choices, categories_folders_names):
    categories.append({
        "model": "api.category",
        "pk": counter,
        "fields": {
            "image": photo_path,
            "name": choices[choice],
        }
    })
    counter += 1

with open('fixtures/categories.json', 'w') as fixture:
    json.dump(categories, fixture)

# ended generating categories
dish_photos_names = {
    "drinks": {
        "coffee": "Кофе",
        "compote": "Компот",
        "kvass": "Квас",
        "lemonade": "Лимонад",
        "mojito": "Мохито"
    },
    "first_courses": {
        "borscht": "Борщ",
        "cheese": "Сырный суп",
        "kharcho": "Суп харчо",
        "peas": "Гороховый суп"
    },
    "salads": {
        "beet": "Винегрет",
        "caesar": "Салат \"Цезарь\"",
        "crab_sticks": "Салат с крабовыми палочками",
        "mimosa": "Салат \"Мимоза\"",
        "olivie": "Салат \"Оливье\""
    },
    "sandwiches": {
        "hot": "Горячий бутерброд",
        "olivie": "Бутерброд с оливье",
        "pizza": "Пицца",
        "sprats": "Гренка со шпротами",
        "toast": "Гренки сырноколбасные"
    },
    "second_courses": {
        "mashed_cutlets": "Котлеты с пюре",
        "pasta": "Макарошки",
        "roll": "Мясной рулет",
        "udon": "Паста удон",
        "vegetable_cutlets": "Овощные котлеты"
    }
}

# generating dishes

# for folder in ['media/images/DishesMenu/' + folder for folder in sorted(os.listdir('media/images/DishesMenu'))]:
#     print(*[f"'': '{item.split('.')[0]}'" for item in sorted(os.listdir(folder))], sep=', ')

dishes = []
counter = 1
category_id = 1
for folder in ['media/images/DishesMenu/' + folder for folder in sorted(os.listdir('media/images/DishesMenu'))]:
    folder_name = folder.split(os.path.sep)[-1]
    categories_folders_names = sorted([f'images/DishesMenu/{folder_name}/{photo}'for photo in os.listdir(folder)])
    item_names = dish_photos_names[folder_name]
    for photo_path in categories_folders_names:
        dishes.append({
            "model": "api.dish",
            "pk": counter,
            "fields": {
                "image": photo_path,
                "name": item_names[photo_path.split(os.path.sep)[-1].split('.')[0]],
                "category_id": category_id,
            }
        })
        counter += 1
    category_id += 1

with open('fixtures/dishes.json', 'w') as fixture:
    json.dump(dishes, fixture)
# end generating dishes
