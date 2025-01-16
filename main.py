from utils.linebot_utils import app

def main():
    print("伺服器啟動中...")
    app.run(port=5000, debug=True)

if __name__ == "__main__":
    main()
