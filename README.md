# AI Twins Work Safety

## 專案簡介
本專案旨在提供工作現場安全管理解決方案，整合法規資料爬取、向量資料庫建立、圖片安全檢測與即時通知功能，藉此協助企業預防安全隱患並遵守相關法規。

## 專案架構
- **core**  
  - 負責核心業務邏輯，包括：  
    - 法規爬取與條文格式化（scraper.py）  
    - 法規向量化及儲存（vectorizer.py）  
    - 根據違規類型查詢相關法規（search_laws.py）
    
- **data**  
  - 存放原始與處理後的 CSV 數據、向量資料庫（Chroma/FAISS）等。

- **models**  
  - 整合圖片檢測模型（YOLOv5 模型與 image_analyzer.py），負責檢測工安圖片中的違規情形。

- **utils**  
  - 通用工具與外部服務整合，包括：  
    - 訊息紀錄工具（logger.py）  
    - Line Bot 與 Flask 網頁服務工具（linebot_utils.py）

- **其他檔案**  
  - 主程式入口（main.py），啟動 Flask 伺服器  
  - 法規爬取程式（scraper_main.py）與向量化程式（vectorizer_main.py）

## 依賴與環境設定
- Python 3.8+
- 需安裝以下主要 Python 套件：
  - flask
  - line-bot-sdk
  - pandas
  - opencv-python
  - torch
  - langchain、langchain_openai、langchain_community
  - beautifulsoup4 等

請先執行以下指令安裝相依套件：
```bash
pip install -r requirements.txt
```

## 啟動專案伺服器（LineBot 工安助手）：
```bash
python main.py
```

## 法規爬取與向量化：
- 執行 scraper_main.py 進行法規爬取及資料清洗
- 執行 vectorizer_main.py 進行法規向量化與資料庫建立

## 貢獻指南
歡迎透過 issue 與 pull request 參與專案開發，請依照專案規範提交修改。

## 授權
本專案採用 MIT 授權，請參閱 LICENSE 檔案以了解詳細資訊。
