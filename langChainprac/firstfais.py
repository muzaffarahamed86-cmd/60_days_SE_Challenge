from langchain_community.embeddings import HuggingFaceEmbeddings # type: ignore
from langchain_community.vectorstores import FAISS

texts = [
    "This is a sample document.", 
    "LangChain makes working with language models easier.", 
    "Embeddings convert text into numerical representations."]

embeded_new = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

vectorstore = FAISS.from_texts(texts, embeded_new)

#vectorstore.save_local("faiss_index")

retriever = vectorstore.as_retriever()
query = "Explain Embedding first and langchain?"
docs = retriever.invoke(query)

for doc in docs:
    print(doc.page_content)

