import sys
import ollama
from vector import get_vector_store, add_pdf_to_vector_store  # function definde in vector.py
import pdfplumber

def get_pdf_summary(pdf_path, maxlen=500):
    with pdfplumber.open(pdf_path) as pdf:
        all_text = "\n".join([page.extract_text() or "" for page in pdf.pages])
    if len(all_text) > maxlen:
        all_text = all_text[:maxlen] + " ...（以下略）"
    prompt = f"以下のPDFの内容を日本語で簡潔に要約してください。:\n{all_text}"
    response = ollama.generate(model=model, prompt=prompt)
    return response["response"].strip()

def get_pdf_headlines(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        all_text="\n".join([page.extract_text() or "" for page in pdf.pages])
    prompt = f"次のPDF本文から、ニュース性・トレンド性のある話題やキーワードを日本語で箇条書きで３つ挙げてください。:\n{all_text[:1000]}"
    response = ollama.generate(model=model, prompt=prompt)
    return response["response"].strip()

if len(sys.argv) < 2:
    print("使い方: python main.py")
else:
    print("こんにちは！質問をどうぞ。終了するには「終了」と入力してください")

model = "hf.co/elyza/Llama-3-ELYZA-JP-8B-GGUF:Q4_K_M"

vector_store = get_vector_store()    # 新規 or 既存DB取得
retriever = vector_store.as_retriever(search_kwargs={"k": 5})
added_pdfs = set()

while True:
    question = input("あなた: ")
    if question.strip() == "終了":
        print("終了します")
        break

    if question.lower().startswith("pdf "):
        pdf_paths = question[4:].strip().replace("\\", "/").split()
        for pdf_path in pdf_paths:
            try:
                if pdf_path not in added_pdfs:
                    print(f"---PDFロード中:{pdf_path}---")
                    add_pdf_to_vector_store(vector_store, pdf_path)
                    added_pdfs.add(pdf_path)
                else:
                    print(f"既に追加済み:{pdf_path}")
                print("\n[PDF要約]")
                print(get_pdf_summary(pdf_path))
                print("\n[ニュース性のある話題]")
                print(get_pdf_headlines(pdf_path))
                print("\nこのPDFに関するご質問があればどうぞ。")
            except Exception as e:
                print("PDFの読み込み／要約に失敗:", e)
            continue

    docs = retriever.invoke(question)
    if not docs:
        prompt = f"PDFから関連情報が見つかりませんでした。質問: {question}"
    else:
        context = "\n-----\n".join(d.page_content for d in docs)
        prompt = f"""あなたは以下のPDF抜粋だけを根拠に、必ず日本語で答えてください。
情報がない場合は「PDFに該当情報はありません」と伝えてください。

[PDF抜粋]
{context}

[質問]
{question}
"""
    response = ollama.generate(model=model, prompt=prompt)
    print("AI:", response["response"].strip())
