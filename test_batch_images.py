from models.image_analyzer import process_images

if __name__ == "__main__":
    # 定義圖片資料夾
    input_dir = "/home/ntc/dino/工安管理/ai-new/data/images"
    output_csv = "/home/ntc/dino/工安管理/ai-new/data/violations.csv"

    print("🚀 開始批量處理影像...")
    process_images(input_dir, output_csv)
    print("✅ 批量處理完成！結果保存到 /home/ntc/dino/工安管理/ai-new/data/violations.csv")
