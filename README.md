# AI 工安管理系統

這是一個利用 AI 技術進行工安違規檢測並提供相關法規匹配的自動化系統。

## 📂 專案架構

```
ai_twins_Work_Safety/
├── core/                      # 核心功能模組
│   ├── vectorizer.py         # 向量化法規資料
│   └── search_laws.py        # 法規搜尋功能
├── utils/                     # 工具模組
│   └── linebot_utils.py      # LineBot 整合
├── data/                      # 資料存放目錄
│   ├── laws.csv              # 法規資料
│   └── chroma_db/            # 向量資料庫
├── vectorizer_main.py         # 向量化主程式
└── README.md                  # 專案說明
```

### 核心模組說明

- **vectorizer.py**: 負責將法規資料向量化並存入 FAISS 資料庫
- **search_laws.py**: 提供法規搜尋功能，將違規行為與相關法規匹配
- **linebot_utils.py**: 整合 LINE Bot 功能，提供使用者查詢介面

## 🔄 處理邏輯

### 資料向量化流程

1. **資料載入**
   - 從 CSV 文件加載法規數據
   - 準備向量化處理
   
2. **向量嵌入**
   - 使用 OpenAI Embeddings 進行向量化
   - 將法規轉換為向量表示
   
3. **向量儲存**
   - 建立 FAISS 向量索引
   - 儲存到本地向量資料庫

### 違規檢測與法規匹配流程

1. **檢測結果處理**
   - 讀取違規檢測 CSV 文件
   - 篩選低置信度項目進行法規匹配
   
2. **法規匹配**
   - 根據違規類型查詢相關法規
   - 使用向量相似度搜尋最相關法條
   
3. **結果輸出**
   - 整合違規信息與法規
   - 輸出至 CSV 文件

### LINE Bot 服務流程

1. **用戶互動**
   - 接收用戶查詢
   - 解析查詢意圖
   
2. **法規搜尋**
   - 調用法規搜尋功能
   - 匹配相關法規條文
   
3. **回覆處理**
   - 格式化法規信息
   - 返回用戶查詢結果

## 🔧 系統需求

- Python 3.8+
- OpenAI API 金鑰
- LINE Messaging API 金鑰 (用於 LINE Bot 功能)
- 相關 Python 套件：
  - langchain
  - openai
  - flask
  - linebot
  - pandas
  - faiss-cpu

## 🚀 使用說明

### 向量化法規資料

```bash
python vectorizer_main.py
```

### 處理違規檢測結果

```bash
python -c "from core.search_laws import process_violations_with_laws; process_violations_with_laws('data/violation_results.csv', 'data/violations_with_laws.csv')"
```

### 啟動 LINE Bot 服務

```bash
export LINE_CHANNEL_SECRET=your_channel_secret
export LINE_CHANNEL_ACCESS_TOKEN=your_channel_access_token
export OPENAI_API_KEY=your_openai_api_key
python app.py
```

## 📊 輸出格式

### 違規檢測結果匹配法規後的 CSV 格式

| 欄位名稱 | 說明 |
|---------|------|
| image_name | 檢測圖片檔名 |
| class | 違規類型 |
| confidence | 檢測置信度 |
| xmin, ymin, xmax, ymax | 違規項目在圖片中的位置 |
| law | 相關法規條文 |
| source | 法規來源 |
| timestamp | 處理時間戳記 |

## ⚠️ 注意事項

- 確保所有 API 金鑰妥善保存，避免硬編碼在程式中
- 處理大量資料時可能需要較長時間，請耐心等待
- 違規檢測結果的準確性會影響法規匹配的相關性
- 定期更新法規資料庫以確保法規的時效性
