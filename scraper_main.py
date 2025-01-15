from core.scraper import fetch_and_clean_data, extract_law_content, save_to_csv, format_law_content

if __name__ == "__main__":
    # 定義法規網址
    url = "https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=N0060014"

    print("🔍 開始爬取法規內容...")
    # 爬取網頁內容
    raw_content = fetch_and_clean_data(url)
    print("✅ 網頁內容爬取成功！")

    print("📋 提取法規條文...")
    # 提取法規的完整內容
    law_content = extract_law_content(raw_content)
    if not law_content:
        print("❌ 未能提取到法規條文，請檢查正則匹配或目標網頁結構！")
    else:
        print("✅ 法規條文提取成功！")

    print("🔄 格式化法規條文...")
    # 將提取的法規條文進行結構化處理
    formatted_records = format_law_content(law_content)
    if not formatted_records:
        print("❌ 法規條文格式化失敗，無法生成結構化數據！")
    else:
        print(f"✅ 成功格式化 {len(formatted_records)} 條條文記錄！")

    # 保存條文至 CSV
    output_csv = "data/laws.csv"
    print(f"💾 保存法規條文至 {output_csv}...")
    save_to_csv(formatted_records, output_csv)
    print("✅ 條文數據已成功保存為 CSV 文件！")
