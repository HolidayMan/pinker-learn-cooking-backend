Base url - `api/v1/`

All the next urls will be relative to base url.

# Categories

`categories/all` **GET** - get all categories *without* it's dishes. Returns array of [Category](./objects.md/#category) objects.

`categories/all/full` **GET** - get all categories *with* it's dishes. Returns array of [CategoryFull](./objects.md/#categoryfull) objects.

`categories/<int>` **GET** - get exact category by it's id. Returns [Category](./objects.md/#category) object.

`categories/<int>/full` **GET** - get name and photo url for the exact category. Returns [CategoryFull](./objects.md/#categoryfull) object.

`categories/<int>/dishes` **GET** - returns array of [DishFull](./objects.md/#dishfull) objects, related to exact category.

# Dishes

`dishes/all` **GET** - get full list of dishes. Returns array of [Dish](./objects.md/#dish) objects.

`dishes/all/full` **GET** - get full list of dishes. Returns array of [DishFull](./objects.md/#dishfull) objects.

`dishes/<int>` **GET** - get exact dish by it's id. Returns [Dish](./objects.md/#dish) object.
 
`dishes/<int>/full` **GET** - get exact dish by it's id. Returns [DishFull](./objects.md/#dishfull) object.

`dishes/<int>/category` **GET** - get exact dish's category. Returns [Category](./objects.md/#category) object.
