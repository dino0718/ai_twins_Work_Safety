from image_analyzer import analyze_image


if __name__ == "__main__":
    # 測試影像路徑
    test_image_path = "/home/ntc/dino/工安管理/ai-new/data/images/w644.jpg"

    print(f"🚀 開始檢測影像：{test_image_path}")
    results = analyze_image(test_image_path)

    # 顯示檢測結果
    print("✅ 檢測結果如下：")
    for result in results:
        print(f"類別：{result['label']}, 信心：{result['confidence']:.2f}, 邊界框：{result['bbox']}")
