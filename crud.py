from sqlalchemy.orm import Session
from models import Ingredient, Recipe, Favorite

# CRUD for Ingredients
def create_ingredient(db: Session, name: str, quantity: int, unit: str):
    ingredient = Ingredient(name=name, quantity=quantity, unit=unit)
    db.add(ingredient)
    db.commit()
    db.refresh(ingredient)
    return ingredient

def update_ingredient(db: Session, ingredient_id: int, quantity: int):
    ingredient = db.query(Ingredient).filter(Ingredient.id == ingredient_id).first()
    if ingredient:
        ingredient.quantity = quantity
        db.commit()
        db.refresh(ingredient)
    return ingredient

def get_all_ingredients(db: Session):
    return db.query(Ingredient).all()

# CRUD for Recipes
def create_recipe(db: Session, name: str, description: str, taste_profile: str, cuisine: str, ingredients: str, instructions: str):
    recipe = Recipe(name=name, description=description, taste_profile=taste_profile, cuisine=cuisine, ingredients=ingredients, instructions=instructions)
    db.add(recipe)
    db.commit()
    db.refresh(recipe)
    return recipe

def get_recipes(db: Session):
    return db.query(Recipe).all()

def get_recipe_by_id(db: Session, recipe_id: int):
    return db.query(Recipe).filter(Recipe.id == recipe_id).first()
