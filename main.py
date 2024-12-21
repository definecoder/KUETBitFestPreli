from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from typing import List
from sqlalchemy.orm import Session
from database import Base, engine, SessionLocal
from crud import create_ingredient, update_ingredient, get_all_ingredients, create_recipe, get_recipes
from models import Ingredient, Recipe

app = FastAPI()


Base.metadata.create_all(bind=engine)

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
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {"Welcome to Define Coders at KUET!"}

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
    
@app.post("/ingredients/")
def add_ingredient(name: str, quantity: int, unit: str, db: Session = Depends(get_db)):
    return create_ingredient(db, name, quantity, unit)

@app.put("/ingredients/{ingredient_id}")
def modify_ingredient(ingredient_id: int, quantity: int, db: Session = Depends(get_db)):
    return update_ingredient(db, ingredient_id, quantity)

@app.get("/ingredients/")
def list_ingredients(db: Session = Depends(get_db)):
    return get_all_ingredients(db)

@app.post("/recipes/")
def add_recipe(name: str, description: str, taste_profile: str, cuisine: str, ingredients: str, instructions: str, db: Session = Depends(get_db)):
    return create_recipe(db, name, description, taste_profile, cuisine, ingredients, instructions)

@app.get("/recipes/")
def list_recipes(db: Session = Depends(get_db)):
    return get_recipes(db)


if __name__ == "__main__":
    print("Starting server...")    
    uvicorn.run(app, host="0.0.0.0", port=8000)    