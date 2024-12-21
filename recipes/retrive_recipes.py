from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import os
from langchain_chroma import Chroma

def retriveRecipe(userQuery: str):

    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")

    embed_model = OpenAIEmbeddings(api_key=api_key)
        
    vector_store = Chroma(
        collection_name="my_fav_recipes",
        embedding_function=embed_model,
        persist_directory="./chroma_langchain_db",
    )
            
    output = vector_store.similarity_search(userQuery, k=4)
    
    combined_knowledge = ""
    for chunk in output:
        combined_knowledge += chunk.page_content
    
    return combined_knowledge    

if __name__ == "__main__":
    print(retriveRecipe("I want to eat pasta."))