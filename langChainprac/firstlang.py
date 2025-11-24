from langchain_community.document_loaders import (TextLoader,PyPDFLoader, ArxivLoader, WikipediaLoader)
from langchain_community.document_loaders import WebBaseLoader


test = TextLoader("notes.txt")
#print(test.load())

text2 =PyPDFLoader("LangChain.pdf")
#print(text2.load())

loader = WebBaseLoader("https://www.geeksforgeeks.org/artificial-intelligence/introduction-to-langchain/")
#docs = loader.load()
#print(loader.load())

text4 = ArxivLoader(query = "1706.03762")
#print(text4.load()) 

text5 = WikipediaLoader(query="Artificial Intelligence", load_max_docs=2)
print(text5.load())