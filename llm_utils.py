from openai import OpenAI

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

def determine_action(user_input):
    """
    使用 LLM 判斷用戶輸入對應的操作
    """
    try:
        prompt = f"""
        用戶輸入: {user_input}
        根據用戶的輸入，請從以下選項中選擇最適合的操作並輸出：
        1. 查詢違規數據
        2. 查詢法規
        3. 分析影像
        4. 寄送違規單
        如果無法判斷，請輸出「未知操作」。
        """
        completion = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "你是一個專業的工安管理助手，幫助用戶選擇合適的操作。"},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in LLM determine_action: {e}")
        return "未知操作"
