from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from typing import List, Optional
from sqlalchemy.orm import Session
from chat.suggestRecipy import suggestRecipy
from database import Base, engine, SessionLocal
from crud import create_ingredient, update_ingredient, get_all_ingredients, create_recipe, get_recipes
from models import Ingredient, Recipe
from recipes.addRecipe import add_recipe_to_chroma
from recipes.retrive_recipes import retriveRecipe

app = FastAPI()


# Base.metadata.create_all(bind=engine)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Welcome to Define Coders at KUET!"}

class Recipe(BaseModel):    
    name: str
    taste: Optional[str] = None
    reviews: Optional[str] = None
    cuisineType: Optional[str] = None
    preparationTime: Optional[str] = None
    ingredients: List[str]
    instructions: Optional[str] = None

@app.post("/recipes")
async def add_recipy_to_db(recipe: Recipe):    
    with open("recipes/my_fav_recipes.txt", "a") as f:
        full_recipy_txt = f"{recipe.name}\n"
        if recipe.taste:
            full_recipy_txt += f"Taste: {recipe.taste}\n"
        if recipe.reviews:
            full_recipy_txt += f"Reviews: {recipe.reviews}\n"
        if recipe.cuisineType:
            full_recipy_txt += f"Cuisine Type: {recipe.cuisineType}\n"
        if recipe.preparationTime:
            full_recipy_txt += f"Preparation Time: {recipe.preparationTime}\n"
        full_recipy_txt += f"Ingredients: {', '.join(recipe.ingredients)}\n"
        if recipe.instructions:
            full_recipy_txt += f"Instructions: {recipe.instructions}\n"
        full_recipy_txt += "\n"
        f.write("\n\n" + full_recipy_txt)    
    f.close()
    
    await add_recipe_to_chroma(full_recipy_txt)
    
    return {"message": "Recipe added successfully"}
    
class IngredientCreate(BaseModel):
    name: str
    quantity: int
    unit: str    

@app.post("/ingredients/")
def add_ingredient(ingredient: IngredientCreate, db: Session = Depends(get_db)):
    return create_ingredient(db, ingredient.name, ingredient.quantity, ingredient.unit)

@app.put("/ingredients/{ingredient_id}")
def modify_ingredient(ingredient_id: int, quantity: int, db: Session = Depends(get_db)):
    return update_ingredient(db, ingredient_id, quantity)

@app.get("/ingredients/")
def list_ingredients(db: Session = Depends(get_db)):
    return get_all_ingredients(db)

@app.get("/recipes")
def list_recipes(db: Session = Depends(get_db)):
    return get_recipes(db)

class ChatRequest(BaseModel):
    query: str

@app.post("/chat/")
async def chat(request: ChatRequest, db: Session = Depends(get_db)):
    query = request.query
    recipes_from_rag = retriveRecipe(query)
    inggredients_available = [inggredient.name for inggredient in get_all_ingredients(db)]
    recipes_from_suggestRecipy = suggestRecipy(query, recipes_from_rag, inggredients_available)
    
    return {"chat_response": recipes_from_suggestRecipy.natural_language_recipe_response, "ingredients_needed_for_recipe": recipes_from_suggestRecipy.natural_language_recipe_ingredients, "recipes_from_rag": recipes_from_rag, "inggredients_available": inggredients_available}


if __name__ == "__main__":
    print("Starting server...")    
    uvicorn.run(app, host="0.0.0.0", port=8000)    