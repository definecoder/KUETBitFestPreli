from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import os
from langchain_chroma import Chroma

def initiateRecipeFromTextFile():
    full_raw_text = ""

    with open('recipes/my_fav_recipes.txt') as f:
        full_raw_text = f.read()
        f.close()    

    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")

    embed_model = OpenAIEmbeddings(api_key=api_key)
    semantic_chunker = SemanticChunker(embed_model, breakpoint_threshold_type="percentile")

    semantic_chunks = semantic_chunker.create_documents([full_raw_text])
    
    print("Number of chunks loaded : ", len(semantic_chunks))
    
    vector_store = Chroma(
        collection_name="my_fav_recipes",
        embedding_function=embed_model,
        persist_directory="./chroma_langchain_db",
    )
    
    vector_store.from_documents(semantic_chunks, embedding=embed_model, persist_directory="./chroma_langchain_db", collection_name="my_fav_recipes")           

if __name__ == "__main__":
    initiateRecipeFromTextFile()