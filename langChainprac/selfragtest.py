from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA # type: ignore
from langchain.vectorstores import FAISS # type: ignore
from langchain.embeddings.openai import OpenAIEmbeddings # type: ignore
from langchain_community.document_loaders import TextLoader
from langchain_community.text_splitter import RecursiveCharacterTextSplitter # type: ignore

