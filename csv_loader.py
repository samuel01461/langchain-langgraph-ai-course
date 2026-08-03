from langchain_community.document_loaders import CSVLoader

loader = CSVLoader(
    file_path="products.csv", 
    csv_args={
        "delimiter": ",",
        "quotechar": "\"",
        "fieldnames": ["product_id", "product_name", "aisle_id", "department_id", "price"]
    },
    encoding="utf-8"
)

docs = loader.load()

print(f"Registros: {len(docs)} em el CSV.")

for doc in docs[:10]: 
    print(doc.page_content)
