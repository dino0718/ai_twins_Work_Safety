from langchain.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import csv
import os

# 初始化 OpenAI API 密鑰
os.environ["OPENAI_API_KEY"] = "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"

def load_laws_from_csv(csv_path):
    """
    從 CSV 文件加載法規數據
    """
    laws = []
    with open(csv_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            laws.append({
                "chapter": row["chapter"],
                "article_number": row["article_number"],
                "content": row["content"]
            })
    return laws

def save_to_vector_db(laws, vector_db_path="data/chroma_db/"):
    """
    將法規內容向量化並存入 FAISS 資料庫
    """
    embeddings = OpenAIEmbeddings()
    texts = [law["content"] for law in laws]
    metadatas = [{"chapter": law["chapter"], "article_number": law["article_number"]} for law in laws]

    vector_db = FAISS.from_texts(texts, embeddings, metadatas=metadatas)
    vector_db.save_local(vector_db_path)
    print(f"✅ 向量資料庫已保存到: {vector_db_path}")
