# Category

Field     | Type        | Desription
:-------- | :---------: | :---------------------------- 
id        | int         | *id* of the category              
name      | string      | *name* of the category. For example `Напитки` 
image_url | string      | *image_url* of category's image 

# CategoryFull
Field     | Type        | Desription
:-------- | :---------: | :---------------------------- 
id        | int         | *id* of the category              
name      | string      | *name* of the category. For example `Салаты` 
image_url | string      | *image_url* of category's image 
dishes    | array       | array of [Dish](#dish) objects 


# Dish

Field     | Type                       | Desription
:-------- | :------------------------: | :---------------------------- 
id        | int                        | *id* of dish              
name      | string                     | *name* of dish. For example `Борщ` 
image_url | string                     | *image_url* of dish's image 
category  | [Category](#category)      | *category* of the dish 


# DishFull

Field        | Type                  | Desription
:----------- | :-------------------: | :---------------------------- 
id           | int                   | *id* of dish              
name         | string                | *name* of dish. For example `Борщ` 
image_url    | string                | *image_url* of dish's image 
category     | [Category](#category) | *category* of the dish 
ingredients  | array                 | *array* of [Ingredient](#ingredient) objects


# Ingredient

Field     | Type                       | Desription
:-------- | :------------------------: | :----------------------------          
name      | string                     | *name* of ingredient. For instance `Крабовые палочки`
amount    | string                     | *amount* of ingredient. For example `200 г` 
dish      | string                     | *image_url* of dish's image
