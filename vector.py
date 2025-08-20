#with assist of perplexity AI https://www.perplexity.ai/search/when-the-code-was-run-i-was-ab-mCNGsVNqTCqoNBBEIFGvtA


# vector.py
from langchain_ollama import OllamaEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import os
import pandas as pd
import pdfplumber

def get_vector_store():
    db_location = "./chroma_langchain_db"
    embeddings = OllamaEmbeddings(model="mxbai-embed-large")
    vector_store = Chroma(
        collection_name="pdf_collection",
        persist_directory=db_location,
        embedding_function=embeddings
    )
    return vector_store


def add_pdf_to_vector_store(vector_store, pdf_path):
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"指定されたPDFファイルが見つかりません: {pdf_path}")

    pages=[]
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages):
            text= page.extract_text() or ""
            pages.append({
                "Title":f"Page{i+1}",
                "Content":text
                })

    df = pd.DataFrame(pages)

    documents = []
    ids = []
    text_cols = [c for c in df.columns if c.lower() not in ["rating", "date"]]
    pdf_id=os.path.basename(pdf_path)

    for i, row in df.iterrows():
        page_content = " ".join([str(row[col]) for col in text_cols if pd.notna(row[col])])
        metadata = {"page": i+1, "source": pdf_path, "pdf_id": pdf_id}
        doc_id = f"{pdf_id}-page{i+1}" 
        documents.append(Document(page_content=page_content, metadata=metadata, id=doc_id))
        ids.append(doc_id)

           
    vector_store.add_documents(documents=documents, ids=ids)



