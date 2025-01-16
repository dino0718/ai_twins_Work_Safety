from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage
import json
import pandas as pd
import os
from openai import OpenAI
from core.search_laws import query_related_laws


# 初始化 Flask 應用
app = Flask(__name__)

# LineBot 配置
CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET", "your_channel_secret")
CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN", "your_channel_access_token")
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)

# OpenAI 配置
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "your_openai_api_key")
client = OpenAI(api_key=OPENAI_API_KEY)

# 工安檢測結果 CSV 文件路徑
VIOLATIONS_CSV_PATH = "/home/ntc/dino/工安管理/ai-new/data/violations_with_laws.csv"

# 用於跟蹤用戶狀態
user_states = {}


@app.route("/", methods=['POST'])
def linebot():
    """
    Line Webhook 處理邏輯，增加狀態跟蹤，實現寄送違規單交互。
    """
    global user_states
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    print(json_data)
    try:
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)

        # 提取用戶訊息
        user_id = json_data['events'][0]['source']['userId']
        tk = json_data['events'][0]['replyToken']
        msg = json_data['events'][0]['message']['text'].strip()

        # 判斷用戶狀態
        if user_id not in user_states:
            user_states[user_id] = {"state": None}  # 初始化狀態

        # 查看違規事件
        if "違規" in msg:
            response_msg = handle_violation_query()
            user_states[user_id]["state"] = "waiting_for_decision"  # 更新狀態
            response_msg += "\n\n是否需要寄送違規單？請回復「是」或「否」。"

        # 判斷是否寄送違規單
        elif user_states[user_id]["state"] == "waiting_for_decision":
            if msg == "是":
                response_msg = send_violation_notice()
                user_states[user_id]["state"] = None  # 重置狀態
            elif msg == "否":
                response_msg = (
                    "請注意，未處理違規可能導致安全事故並違反相關法規。"
                    "建議您儘快採取行動。"
                )
                user_states[user_id]["state"] = None  # 重置狀態
            else:
                response_msg = "請回復「是」或「否」以確認是否寄送違規單。"

        # 預設回應
        else:
            response_msg = "歡迎使用工安管理助手，您可以查詢違規數據或寄送違規單。"

        # 回覆用戶
        text_message = TextSendMessage(text=response_msg)
        line_bot_api.reply_message(tk, text_message)

    except Exception as e:
        print(f"Error: {e}")
        return "Error: {e}", 500
    return "OK"





def handle_violation_query():
    """
    處理違規數據查詢，生成包含法條與建議的回應，由 LLM 動態生成。
    """
    if not os.path.exists(VIOLATIONS_CSV_PATH):
        return "違規數據尚未生成，請稍後再試。"

    # 加載違規數據
    df = pd.read_csv(VIOLATIONS_CSV_PATH)

    # 統計違規次數
    violation_counts = df["class"].value_counts()
    primary_violation = violation_counts.index[0]  # 使用主要違規類型作為關鍵字

    # 查詢相關法條
    laws = query_related_laws(primary_violation)

    # 構造傳遞給 LLM 的上下文
    law_details = "\n".join(
        [f"{i+1}. {law['law']}" for i, law in enumerate(laws)]
    )
    violation_stats = "\n".join(
        [f"- {cls}: {count} 次" for cls, count in violation_counts.items()]
    )

    # 構建 LLM 的 Prompt
    prompt = f"""
根據以下數據，請生成一份完整的回應，內容包括違規統計、相關法條，以及改進建議：

違規數據統計：
{violation_stats}

相關法條：
{law_details}

### 要求：
1. 使用專業且易於理解的語言。
2. 將違規數據與相關法條聯繫起來。
3. 提供2個具體、可執行的改進建議，並詢問是否需要協助寄送違規單。
    """
    try:
        # 調用大語言模型生成回應
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "你是一個專業的工安管理助理，幫助用戶分析違規數據並提供改進建議。"},
                {"role": "user", "content": prompt}
            ]
        )
        response_msg = completion.choices[0].message.content
        return response_msg
    except Exception as e:
        print(f"Error while calling GPT: {e}")
        return "很抱歉，無法處理您的請求，請稍後再試。"
    

def send_violation_notice():
    """
    使用大語言模型生成違規單發送回覆。
    """
    # 構建 LLM 的 Prompt
    prompt = """
請生成一條簡短但專業的回應，告知用戶違規單已通過系統成功發送。
    """
    try:
        # 調用大語言模型生成回應
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "你是一個專業的工安管理助理，幫助用戶生成違規單發送確認信息。"},
                {"role": "user", "content": prompt}
            ]
        )
        response_msg = completion.choices[0].message.content
        return response_msg
    except Exception as e:
        print(f"Error while calling GPT: {e}")
        return "很抱歉，目前無法發送違規單，請稍後再試。"







def handle_gpt_chat(user_message):
    """
    使用 OpenAI GPT 進行聊天
    """
    try:
        completion = client.chat.completions.create(
            model="gpt-4o",  # 替換為您使用的模型
            messages=[
                {"role": "system", "content": "你是一個專業的工安助手，能夠回答與工安相關的問題。"},
                {"role": "user", "content": user_message}
            ]
        )
        response_msg = completion.choices[0].message.content
        return response_msg
    except Exception as e:
        print(f"Error while calling GPT: {e}")
        return "很抱歉，無法處理您的請求，請稍後再試。"


@app.route("/", methods=['GET'])
def home():
    return "LineBot 工安助手已啟動"



