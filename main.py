from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel
from typing import List

app = FastAPI()

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


if __name__ == "__main__":
    print("Starting server...")    
    uvicorn.run(app, host="0.0.0.0", port=8000)    