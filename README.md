# 法規爬蟲工具

這是一個專門用於抓取台灣法務部法規資料庫的自動化工具，可以將法規內容結構化並匯出成易於分析的格式。

## 📂 專案架構

```
ai-new/
├── core/               # 核心功能模組
│   ├── scraper.py     # 爬蟲核心邏輯
│   └── server.py      # API服務器邏輯
├── data/              # 資料存放目錄
│   └── laws.csv       # 輸出的法規資料
├── scraper_main.py    # 主程式入口
├── server_main.py     # 服務器入口
└── requirements.txt   # 相依套件清單
```

### 核心模組說明
- `scraper.py`: 包含資料爬取、清理和格式化的核心功能
- `scraper_main.py`: 爬蟲程式進入點
- `server.py`: 包含 RESTful API 實作
- `server_main.py`: API伺服器進入點

## 🔄 處理邏輯

### 資料擷取流程
1. **網頁爬取**
   - 發送請求到法務部法規網站
   - 取得原始HTML內容
   
2. **資料解析**
   - 清理HTML標記
   - 提取法規條文內容
   
3. **結構化處理**
   - 分離條號與條文
   - 整理附註資訊
   
4. **資料儲存**
   - 轉換成CSV格式
   - 寫入檔案系統

### API服務流程
1. **資料載入**
   - 讀取已爬取的CSV資料
   - 建立資料索引
   
2. **API端點**
   - `/api/laws`: 獲取所有法規列表
   - `/api/laws/<id>`: 獲取特定條文
   - `/api/search`: 關鍵字搜尋

3. **外部存取**
   - 通過ngrok建立安全通道
   - 產生公開存取URL

### 錯誤處理機制
- 網路連線異常處理
- 解析失敗補救措施
- 資料完整性驗證

## 🔧 系統需求

- Python 3.6+
- 相關套件需求請參考 `requirements.txt`
- ngrok

## 🚀 使用說明

### 安裝步驟

1. 下載專案
```bash
git clone [repository-url]
cd ai-new
```

2. 建立虛擬環境
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. 安裝相依套件
```bash
pip install -r requirements.txt
```

### 執行方式

1. 設定目標法規
```python
url = "https://law.moj.gov.tw/LawClass/LawAll.aspx?pcode=N0060014"
```

2. 執行爬蟲
```bash
python scraper_main.py
```

### 啟動服務器

1. 啟動API服務器
```bash
python server_main.py
```

2. 啟動ngrok通道
```bash
ngrok http 5000
```

服務器預設設定：
- 本地端口: 5000
- API文件: http://localhost:5000/docs
- 健康檢查: http://localhost:5000/health

### API使用範例

獲取所有法規：
```bash
curl http://localhost:5000/api/laws
```

搜尋特定條文：
```bash
curl http://localhost:5000/api/search?keyword=安全
```

## 📊 輸出格式

CSV檔案結構：
- 條號 (Article_ID)
- 條文內容 (Content)
- 附註說明 (Notes)

## ⚠️ 注意事項

1. 請遵守法務部網站使用規範
2. 建議設定適當的爬取延遲時間
3. 僅供學術研究使用

## 📝 授權說明

本專案採用 MIT 授權條款 - 詳見 [LICENSE](LICENSE) 檔案

## 📮 聯絡方式

如有任何問題，請聯繫專案維護者 [your-email@example.com]