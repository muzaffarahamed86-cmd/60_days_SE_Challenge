from langchain_openai import OpenAIEmbeddings # type: ignore

from langchain_community.embeddings import HuggingFaceEmbeddings # type: ignore

embeded2 = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

emb = OpenAIEmbeddings(
    model="text-embedding-3-small",
    api_key="YOUR_OPENAI_API_KEY"  # Replace with your actual API key or use environment variable
)

textembed = "This is one of the most wonderful generative AI Course."


embeded = embeded2.embed_query(textembed)
print(embeded[:5])
