from langchain_community.document_loaders import PyPDFLoader

splittext = PyPDFLoader("LangChain.pdf")
full_text = splittext.load()
print(full_text)