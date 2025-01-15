from core.vectorizer import load_laws_from_csv, save_to_vector_db

if __name__ == "__main__":
    csv_path = "data/laws.csv"  # 爬取並保存的法規數據
    vector_db_path = "data/chroma_db/"

    # 加載法規數據
    laws = load_laws_from_csv(csv_path)
    print(f"加載到 {len(laws)} 條法規數據。\n")

    # 存入向量資料庫
    save_to_vector_db(laws, vector_db_path)
