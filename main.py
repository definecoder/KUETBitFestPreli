from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

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
    recipeName: str
    taste: Optional[str] = None
    reviews: Optional[str] = None
    cuisineType: Optional[str] = None
    preparationTime: Optional[str] = None
    ingredients: List[str]
    instructions: Optional[str] = None

@app.post("/add-recipe")
def add_recipy_to_db(recipe: Recipe):    
    with open("recipes/my_fav_recipes.txt", "a") as f:
        f.write(f"{recipe.recipeName}\n")
        if recipe.taste:
            f.write(f"Taste: {recipe.taste}\n")
        if recipe.reviews:
            f.write(f"Reviews: {recipe.reviews}\n")
        if recipe.cuisineType:
            f.write(f"Cuisine Type: {recipe.cuisineType}\n")
        if recipe.preparationTime:
            f.write(f"Preparation Time: {recipe.preparationTime}\n")
        f.write(f"Ingredients: {', '.join(recipe.ingredients)}\n")
        if recipe.instructions:
            f.write(f"Instructions: {recipe.instructions}\n")
        f.write("\n")
    
    f.close()
    return


class RecipeRequest(BaseModel):
    ingredients: List[str]
    name: str

class RecipeResponse(BaseModel):
    id: int
    name: str
    ingredients: List[str]

@app.post("/generate-recipe", response_model=RecipeResponse)
def generate_recipe(data: RecipeRequest):
    try:
        ingredients = data["ingredients"]
        recipe = {
            "id": 1,
            "name": data["name"],
            "ingredients": ingredients
        }
        return {"recipe": recipe}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("Starting server...")    
    uvicorn.run(app, host="0.0.0.0", port=8000)    