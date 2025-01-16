from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
import os
import csv
from pathlib import Path
from datetime import datetime

os.environ["OPENAI_API_KEY"] = "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"  # 替換為您的 API 密鑰

# 加載向量資料庫
VECTOR_DB_PATH = "/home/ntc/dino/工安管理/ai-new/data/chroma_db"  # 修改為你的資料庫位置
embedding = OpenAIEmbeddings()  # 使用 OpenAI 的嵌入模型
vector_db = FAISS.load_local(VECTOR_DB_PATH, embedding, allow_dangerous_deserialization=True)

def query_related_laws(violation_type, k=3):
    """
    根據違規類型查詢法規條文。
    :param violation_type: 違規類型（例如 "helmet", "vest"）。
    :param k: 返回相關法規的數量。
    :return: 包含法規內容和來源的列表。
    """
    results = vector_db.similarity_search(violation_type, k=k)
    return [{"law": r.page_content, "source": r.metadata.get("source", "unknown")} for r in results]

def process_violations_with_laws(results_file, output_file):
    """
    根據檢測結果匹配相關法規，並保存到新的 CSV 文件中。
    只處理信心值低於 70 分的資料。
    :param results_file: 檢測結果文件的路徑（CSV 格式）。
    :param output_file: 輸出文件的路徑（CSV 格式）。
    """
    # 檢查檢測結果文件是否存在
    results_path = Path(results_file)
    if not results_path.exists():
        raise FileNotFoundError(f"檢測結果文件不存在：{results_file}")

    # 創建輸出目錄
    output_path = Path(output_file)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    # 讀取檢測結果並匹配法規
    with open(results_file, mode="r", encoding="utf-8") as csvfile, \
         open(output_file, mode="w", newline="", encoding="utf-8") as outfile:
        reader = csv.DictReader(csvfile)
        fieldnames = ["image_name", "class", "confidence", "xmin", "ymin", "xmax", "ymax", "law", "source", "timestamp"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            # 只處理信心值低於 70 的違規項目
            if float(row["confidence"]) < 70:
                violation_type = row["class"]
                related_laws = query_related_laws(violation_type)
                for law in related_laws:
                    writer.writerow({
                        "image_name": row["image_name"],
                        "class": row["class"],
                        "confidence": row["confidence"],
                        "xmin": row["xmin"],
                        "ymin": row["ymin"],
                        "xmax": row["xmax"],
                        "ymax": row["ymax"],
                        "law": law["law"],
                        "source": law["source"],
                        "timestamp": datetime.now().isoformat()
                    })
    print(f"✅ 匹配結果已保存到：{output_file}")



def main():
    # Example usage
    results_file = "/home/ntc/dino/工安管理/ai-new/data/results.csv"  # 修改為你的檢測結果文件路徑
    output_file = "/home/ntc/dino/工安管理/ai-new/data/violations_with_laws.csv"  # 修改為你的輸出文件路徑
    process_violations_with_laws(results_file, output_file)

if __name__ == "__main__":
    main()
