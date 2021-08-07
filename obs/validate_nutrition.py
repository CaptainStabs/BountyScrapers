nutrition_fields = ["calories", "fat_g", "carbohydrates_g", "protein_g", "sodium_mg", "price_usd","cholesterol_mg", "fiber_g", "sugars_g" ]

def validateNoUnitsInCells(row):
    for field in nutrition_fields:
        fieldName = (f'{field!r}').replace("'", "")
        value = row[fieldName]
        stripped = value.replace("mg", "").replace("g", "").replace("(", "").replace(")","").strip()
        if stripped != value:
            print(f'UPDATE menu_items SET name={stripped!r} WHERE name = {value!r}')
            print(f"DELETE FROM menu_items WHERE name = {value!r}")

def validateNutrition(row):
    validateNoUnitsInCells(row)