from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os
os.environ["OPENAI_API_KEY"] = "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"  # 替換為您的 API 密鑰

# 加載向量資料庫
VECTOR_DB_PATH = "/home/ntc/dino/工安管理/ai-new/data/chroma_db"  # 修改為你的資料庫位置
embedding = OpenAIEmbeddings()  # 使用 OpenAI 的嵌入模型
vector_db = FAISS.load_local(VECTOR_DB_PATH, embedding, allow_dangerous_deserialization=True)

def query_related_laws(violation_type):
    """
    根據違規類型查詢法規條文
    """
    # 查詢向量資料庫
    results = vector_db.similarity_search(violation_type, k=3)  # 返回 3 條相關條文
    return [{"law": r.page_content, "source": r.metadata.get("source", "unknown")} for r in results]
