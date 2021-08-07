# Menus

`menus` is a database catalog of menu items, and their nutritional information and price, for restaurants in the United States. 

The schema of the `menu_items` table has a 3-part composite primary key of (`name`, `restaurant_name` and `identifier`).

```
menus> describe menu_items;
+-----------------+---------------+------+-----+---------+-------+
| Field           | Type          | Null | Key | Default | Extra |
+-----------------+---------------+------+-----+---------+-------+
| name            | varchar(255)  | NO   | PRI |         |       |
| restaurant_name | varchar(100)  | NO   | PRI |         |       |
| identifier      | varchar(255)  | NO   | PRI |         |       |
| calories        | int           | YES  |     | NULL    |       |
| fat_g           | decimal(6,2)  | YES  |     | NULL    |       |
| carbohydrates_g | int           | YES  |     | NULL    |       |
| protein_g       | int           | YES  |     | NULL    |       |
| sodium_mg       | int           | YES  |     | NULL    |       |
| price_usd       | decimal(10,2) | YES  |     |         |       |
| cholesterol_mg  | int           | YES  |     | NULL    |       |
| fiber_g         | int           | YES  |     | NULL    |       |
| sugars_g        | int           | YES  |     | NULL    |       |
+-----------------+---------------+------+-----+---------+-------+
```

### How to construct  3-part composite primary key
* `name` is the name of an individual item
* `restaurant_name` is the name of the restaurant for whose menu items are being submitted
* `identifier` is a unique string consisting of city and state, where applicable, or `national` if it is a country wide menu.
     * For menus associated with a specific city, the `identifier` should look like this, for example: `Santa Monica, CA`
     * For menus delineated by state, the `identifier` would be `NULL, CA`
     * For national menus,  use just one word in the `identifier` field: `NATIONAL`
     * For menus sourced from delivery service menus, put the service name as the identifier: `POSTMATES`, `UBEREATS`, etc.
        * If the menu is at the state or city level append them to the service name, comma delineated: `POSTMATES, SANTA MONICA, CA` OR `UBEREATS, CA`
