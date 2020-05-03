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

# generating ingredients


class Dish:
    objects = dishes

    def __init__(self, name, photo_path, ingredients):
        self.name = name
        if not photo_path.startswith('images'):
            self.image = os.path.join('images', 'DishesMenu', photo_path)
        else:
            self.image = photo_path
        self.ingredients = ingredients
        for ingredient in self.ingredients:
            ingredient.dish = self
            DishIngredient(self, ingredient, ingredient.amount)

    def get_json(self):
        for dish in dishes:
            if dish['fields']['image'] == self.image:
                return dish


class Ingredient:
    objects = []

    def __init__(self, name, amount):
        self.name = name
        self.amount = amount

        for ingredient in self.objects:
            if ingredient['fields']['name'] == self.name:
                break
        else:
            self.objects.append(self.get_json())

    def get_json(self):
        for ingredient in self.objects:
            if ingredient['fields']['name'] == self.name:
                return ingredient
        else:
            return {
                "model": "api.ingredient",
                "pk": len(self.objects) + 1,
                "fields": {
                    "name": self.name,
                }
            }


class DishIngredient:
    objects = []

    def __init__(self, dish, ingredient, amount):
        self.dish_id = dish.get_json()['pk']
        self.ingredient_id = ingredient.get_json()['pk']
        self.amount = amount

        for obj in self.objects:
            if obj['fields']['dish_id'] == self.dish_id and obj['fields']['ingredient_id'] == self.ingredient_id:
                break
        else:
            self.objects.append(self.get_json())

    def get_json(self):
        for obj in self.objects:
            if obj['fields']['dish_id'] == self.dish_id and obj['fields']['ingredient_id'] == self.ingredient_id:
                return obj
        else:
            return {
                "model": "api.dishingredient",
                "pk": len(self.objects) + 1,
                "fields": {
                    "dish_id": self.dish_id,
                    "ingredient_id": self.ingredient_id,
                    "amount": self.amount,
                }
            }


drinks = [
  Dish('Компот', 'drinks/compote.jpg', [
    Ingredient('Вишня', '50 г'),
    Ingredient('Сахар', '10 г'),
    Ingredient('Лимонная кислота', '30 г'),
    Ingredient('Вода', '2 л')
  ]),
  Dish('Лимонад', 'drinks/lemonade.jpg', [
    Ingredient('Лимон', '1 шт'),
    Ingredient('Сахар', '120 г'),
    Ingredient('Вода', '800 г'),
  ]),
  Dish('Мохито', 'drinks/mojito.jpg', [
    Ingredient('Лайм', '3 шт'),
    Ingredient('Сахар тростниковый', '40 г'),
    Ingredient('Мята свежая', '20 листиков'),
    Ingredient('Ром белый', '50 г'),
    Ingredient('Вода газированная', '2 л'),
    Ingredient('Лед', '4 кубика'),
  ]),
  Dish('Кофе со сгущенкой', 'drinks/coffee.jpg', [
    Ingredient('Эспрессо', '1 стакан'),
    Ingredient('Сгущенное молоко', '25 г'),
    Ingredient('Лед', '5 кубиков'),
    Ingredient('Шоколадный сироп', '12 г')
  ]),
  Dish('Квас', 'drinks/kvass.jpg', [
    Ingredient('Сухари ржаные', '200 г'),
    Ingredient('Дрожжи', '25 г'),
    Ingredient('Сахар', '50 г'),
    Ingredient('Изюм', '40 г')
  ])
]
sandwiches = [
  Dish('Гренки сырноколбасные', 'sandwiches/toast.jpg', [
    Ingredient('Хлеб белый', '1 батон'),
    Ingredient('Колбаса', '200 г'),
    Ingredient('Сыр твердый', '100 г'),
    Ingredient('Яйца', '2 шт'),
    Ingredient('Молоко', '60 г'),
    Ingredient('Масло подсолнечное', '60 г')
  ]),
  Dish('Горячие с чесноком', 'sandwiches/hot.jpg', [
    Ingredient('Сыр плавленный', '2 шт'),
    Ingredient('Майонез', '20 г'),
    Ingredient('Яйца', '1 шт'),
    Ingredient('Хлеб', '9 кусков'),
    Ingredient('Чеснок', '3 шт')
  ]),
  Dish('Бутеры со шпротами', 'sandwiches/sprats.jpg', [
    Ingredient('Батон нарезанный', '15 шт'),
    Ingredient('Шпроты ', '1 шт'),
    Ingredient('Яйца вареные', '3 шт'),
    Ingredient('Огурец', '1 шт'),
    Ingredient('Помидоры', '5 шт')
  ]),
  Dish('Бутеры с оливье', 'sandwiches/olivie.jpg', [
    Ingredient('Батон', '200 г'),
    Ingredient('Крабовые палочки', '100 г'),
    Ingredient('Огурец', '1 шт'),
    Ingredient('Сыр плавленый', '90 г'),
    Ingredient('Укроп', '2 шт'),
    Ingredient('Масло сливочное', '10 г'),
    Ingredient('Майонез', '30 г'),
    Ingredient('Соль', '30 г')
  ]),
  Dish('Пицца на хлебе', 'sandwiches/pizza.jpg', [
    Ingredient('Хлеб', '4 куска'),
    Ingredient('Ветчина', '150 г'),
    Ingredient('Сыр твердый', '150 г'),
    Ingredient('Майонез', '20 г'),
    Ingredient('Кетчуп', '20 г'),
    Ingredient('Зелень', '5 шт')
  ])
]
salads = [
  Dish('С крабовыми палочками', 'salads/crab_sticks.jpg', [
    Ingredient('Крабовые палочки', '200 г'),
    Ingredient('Огурцы маринованные', '2 шт'),
    Ingredient('Лук репчатый', '1 шт'),
    Ingredient('Морковь', '1 шт'),
    Ingredient('Картофель', '4 шт'),
    Ingredient('Горошек консервированный', '100 г'),
    Ingredient('Яйца куриные', '2 шт'),
    Ingredient('Майонез', '150 г')
  ]),
  Dish('Cвекольный салат', 'salads/beet.jpg', [
    Ingredient('Свекла', '3 шт'),
    Ingredient('Огурцы соленые', '4 г'),
    Ingredient('Горошек зеленый консервированный', '70 г'),
    Ingredient('Масло подсолнечное', '20 г'),
    Ingredient('Сок лимонный', '40 г'),
    Ingredient('Соль', '10 г')
  ]),
  Dish('Оливье', 'salads/olivie.jpg', [
    Ingredient('Картофель', '7 шт'),
    Ingredient('Морковь', '5 шт'),
    Ingredient('Маринованные огурцы', '6 шт'),
    Ingredient('Консервированный зеленый горошек', '1 шт'),
    Ingredient('Яйцо куриное', '4 шт'),
    Ingredient('Докторская колбаса', '300 г'),
    Ingredient('Сметана', '200 г'),
    Ingredient('Майонез', '100 г')
  ]),
  Dish('Цезарь', 'salads/caesar.jpg', [
    Ingredient('Филе куриное', '150 г'),
    Ingredient('Листья салата ', '150 г'),
    Ingredient('Помидор', '8 шт'),
    Ingredient('Пармезан', '20 г'),
    Ingredient('Хлеб ', '2 шт'),
    Ingredient('Перец', '1 шт'),
    Ingredient('Соль', '2 шт')
  ]),
  Dish('Мимоза', 'salads/mimosa.jpg', [
    Ingredient('Рыба консервированная в масле', '1 голова'),
    Ingredient('Картофель', '3 шт'),
    Ingredient('Яйца куриные', '2 шт'),
    Ingredient('Морковь', '1 шт'),
    Ingredient('Лук репчатый', '2 шт'),
    Ingredient('Майонез', '10 г'),
    Ingredient('Соль', '10 г')
  ])
]
secondCourses = [
  Dish('Котлеты с пюре', 'second_courses/mashed_cutlets.jpg', [
    Ingredient('Фарш', '300 г'),
    Ingredient('Яйцо куриное', '1 шт'),
    Ingredient('Мука пшеничная', '30 г'),
    Ingredient('Масло растительное', '30 г'),
    Ingredient('Перец черный молотый', '1 шт'),
    Ingredient('Картофель', '3 шт'),
    Ingredient('Молоко', '2 л')
  ]),
  Dish('Лапша удон', 'second_courses/udon.jpg', [
    Ingredient('Лапша пшеничная', '150 г'),
    Ingredient('Куриное филе', '150 г'),
    Ingredient('Морковь', '3 шт'),
    Ingredient('Лук репчатый', '2 шт'),
    Ingredient('Перец желтый сладкий', '3 шт'),
    Ingredient('Чеснок', '1 шт'),
    Ingredient('Имбирь', '12 шт'),
    Ingredient('Соевый соус', '20 г'),
    Ingredient('Сельдерей', '1 шт'),
    Ingredient('Масло растительное', '1 л')
  ]),
  Dish('Куриные рулеты с грибами', 'second_courses/roll.jpg', [
    Ingredient('Куриная грудка', '300 г'),
    Ingredient('Шампиньоны', '100 г'),
    Ingredient('Лук репчатый', '1 шт'),
    Ingredient('Картофель', '2 шт'),
    Ingredient('Перец черный молотый', '1 шт'),
    Ingredient('Молотая паприка', '1 шт')
  ]),
  Dish('Котлеты из овощей', 'second_courses/vegetable_cutlets.jpg', [
    Ingredient('Кабачки', '2 шт'),
    Ingredient('Оливковое масло', '30 г'),
    Ingredient('Картофель', '2 шт'),
    Ingredient('Помидоры', '4 шт'),
    Ingredient('Лук репчатый', '2 шт'),
    Ingredient('Яйцо куриное', '2 шт'),
    Ingredient('Мука пшеничная', '60 г')
  ]),
  Dish('Паста с помидорами', 'second_courses/pasta.jpg', [
    Ingredient('Макаронные изделия', '20 г'),
    Ingredient('Черри', '1 шт'),
    Ingredient('Чеснок', '1 шт'),
    Ingredient('Оливковое масло', '1 шт'),
    Ingredient('Базилик', '3 шт')
  ])
]
firstCourses = [
  Dish('Борщ с говядиной', 'first_courses/borscht.png', [
    Ingredient('Говядина', '500 г'),
    Ingredient('Свёкла', '1 шт'),
    Ingredient('Картофель', '2 шт'),
    Ingredient('Капуста', '200 г'),
    Ingredient('Морковь', '1 шт'),
    Ingredient('Лук', '1 шт'),
    Ingredient('Зелень', '30 г'),
    Ingredient('Томатная паста', '10 г'),
    Ingredient('Масло растительное', '2 шт')
  ]),
  Dish('Харчо', 'first_courses/kharcho.jpg', [
    Ingredient('Курица', '1 голова'),
    Ingredient('Рис', '10 г'),
    Ingredient('Чеснок', '1 шт'),
    Ingredient('Масло сливочное', '50 г')
  ]),
  Dish('Суп с плавленым сыром', 'first_courses/cheese.jpg', [
    Ingredient('Куриное филе', '500 г'),
    Ingredient('Сыр плавленый ', '20 г'),
    Ingredient('Вермишель', '100 г'),
    Ingredient('Картофель', '4 шт'),
    Ingredient('Лук репчатый', '1 шт'),
    Ingredient('Морковь', '1 шт'),
    Ingredient('Масло сливочное', '20 г')
  ]),
  Dish('Гороховый суп', 'first_courses/peas.jpg', [
    Ingredient('свиные ребра', '1 шт'),
    Ingredient('копчености', '20 г'),
    Ingredient('горох колотый', '30 г'),
    Ingredient('Морковь', '4 шт'),
    Ingredient('Лук репчатый', '5 шт'),
    Ingredient('Картофель', '6 шт'),
  ])
]


with open('fixtures/dishingredient.json', 'w') as fixture:
    json.dump(DishIngredient.objects, fixture)

with open('fixtures/ingredient.json', 'w') as fixture:
    json.dump(Ingredient.objects, fixture)
