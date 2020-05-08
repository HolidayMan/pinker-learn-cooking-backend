Base url - `api/v1/`

All the next urls will be relative to base url

# Categories
`categories/all` **GET** - get all categories *without* it's dishes. Returns array of [Category](./objects.md/#category) objects

`categories/all/full` **GET** - get all categories *with* it's dishes. Returns array of [CategoryFull](./objects.md/#categoryfull) objects

`categories/<int>` **GET** - get exact category by it's id. Returns [Category](./objects.md/#category) object

`categories/<int>/full` **GET** - get name and photo url for the exact category

`categories/<int>/dishes` **GET** - returns array of [Dish](./objects.md/#dish) objects, related to exact category

`categories/<int>/dishes/full` **GET** - returns array of [DishFull](./objects.md/#dishfull) objects, related to exact category

# Dishes

`dishes/all` **GET** - get full list of dishes *without* included parameters like ingredients etc. Returns array of [Dish](./objects.md/#dish) objects

`dishes/all/full` **GET** - get full list of dishes *with* all included parameters
 like ingredients etc.

`dishes/<int>` **GET** - get exact dish by it's id

`dishes/<int>/info` **GET** - get name, category and photo url for the
 exact dish 
 
`dishes/<int>/category` **GET** - get exact dish's category

`dishes/<int>/ingredients` **GET** - get exact dish's ingredients
