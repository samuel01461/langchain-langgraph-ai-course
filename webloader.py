from langchain_community.document_loaders import WebBaseLoader

loader = WebBaseLoader("https://www.nic.ar")
data = loader.load()
print(data)