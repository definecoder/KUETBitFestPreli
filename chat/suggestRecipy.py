import os
from dotenv import load_dotenv
from pydantic import BaseModel
from openai import OpenAI
from typing import List

load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=openai_api_key)

    
class RecipeResponse(BaseModel):
    natural_language_recipe_response: str
    natural_language_recipe_ingredients: List[str]
    
def suggestRecipy(userQuery: str, recipies: List[str], ingredients: List[str]) -> RecipeResponse:

    prompt = f"""
    # Here is a list of recipes:
    {recipies}
    
    # Here is a list of ingredients that the user has:
    {ingredients}
    
    # And here is the user's query:
    {userQuery}
    
    # Please provide a recipe suggestion based on the user's query and their mood.
    """
        

    completion = client.beta.chat.completions.parse(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": """You are a cooking recipe suggestion bot.
             You will be given a list of recipes and ingredients. You need to suggest a recipe based on the user query.
             Consider the users query and users mood to suggest a recipe.
             You will be provided with a list of recipes and ingredients.
             """},
            {"role": "user", "content": prompt}
        ],
        response_format=RecipeResponse,
    )    
    
    recipe_suggestion = completion.choices[0].message.parsed    

    return recipe_suggestion