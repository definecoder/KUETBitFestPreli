from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings
from dotenv import load_dotenv
import os
from langchain_chroma import Chroma

def retriveRecipe():    

    load_dotenv()
    api_key = os.environ.get("OPENAI_API_KEY")

    embed_model = OpenAIEmbeddings(api_key=api_key)
        
    vector_store = Chroma(
        collection_name="my_fav_recipes",
        embedding_function=embed_model,
        persist_directory="./chroma_langchain_db",
    )
        
    semantic_chunk_retriever = vector_store.as_retriever(search_kwargs={"k" : 2})
    output = semantic_chunk_retriever.invoke("I want to eat breakfast and I have fish fillets, potatoes.")
    
    print("output : ")
    print(output)

    for chunk in output:        
        print(chunk.page_content)
        print("\n\n\n\n")

if __name__ == "__main__":
    retriveRecipe()