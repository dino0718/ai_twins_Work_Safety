from models.image_analyzer import process_images_with_laws

if __name__ == "__main__":
    input_dir = "data/images"                  # 測試圖片目錄
    output_csv = "data/violations_with_laws.csv"  # 輸出 CSV 文件

    print("🚀 開始批量檢測影像並查詢法規條文...")
    process_images_with_laws(input_dir, output_csv)
    print("✅ 檢測與法規查詢完成！結果已保存到 data/violations_with_laws.csv")
