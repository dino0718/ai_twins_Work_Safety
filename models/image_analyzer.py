import sys
import os
import torch
import cv2
import pandas as pd
from datetime import datetime


# 添加 YOLOv5 文件夾到 Python 搜索路徑
YOLOV5_PATH = os.path.join(os.path.dirname(__file__), 'yolov5')
sys.path.append(YOLOV5_PATH)
sys.path.append(os.path.join(YOLOV5_PATH, 'utils'))  # 確保 YOLOv5 的 utils 被正確引用
from yolov5.models.common import DetectMultiBackend


# 模型路徑
MODEL_PATH = "/home/ntc/dino/工安管理/ai-new/models/best.pt"

# 加載 YOLO 模型
device = torch.device('cpu')  # 或 'cuda' 如果您有 GPU
model = DetectMultiBackend(MODEL_PATH, device=device)
print(f"✅ 成功加載模型：{MODEL_PATH}")

# results = model('/home/ntc/dino/工安管理/ai-new/data/images/186510343_1816338865193347_2587363028274937400_n.jpg')  # 替換為您要測試的圖像路徑
# results.show()  # 顯示推理結果

# 定義影像分析函數
def analyze_image(image_path):
    """
    使用本地 YOLOv5 模型分析影像並檢測違規行為。
    """
    # 加載影像並轉換格式
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"無法加載影像：{image_path}")
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 轉為 RGB 格式

    # 使用模型進行推論
    results = model(img)

    # 確認返回的結果
    print("模型推論結果：", results)

    # 提取檢測結果
    try:
        detections = results.pandas().xyxy[0]  # 檢測結果為 Pandas DataFrame
    except Exception as e:
        raise ValueError(f"檢測結果提取失敗：{e}")

    violations = []
    for _, row in detections.iterrows():
        violations.append({
            "label": row['name'],  # 類別名稱
            "confidence": row['confidence'],  # 信心分數
            "bbox": [row['xmin'], row['ymin'], row['xmax'], row['ymax']]  # 邊界框座標
        })

    return violations




def process_images(input_dir, output_csv="/home/ntc/dino/工安管理/ai-new/data/violations.csv"):
    """
    批量處理影像，檢測違規行為並保存結果到 CSV。
    """
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    all_violations = []

    # 遍歷輸入資料夾中的圖片
    for filename in os.listdir(input_dir):
        filepath = os.path.join(input_dir, filename)
        if filepath.lower().endswith(('.jpg', '.png', '.jpeg')):
            results = analyze_image(filepath)  # 單張圖片檢測
            for result in results:
                all_violations.append({
                    "image_id": filename,
                    "timestamp": datetime.now().isoformat(),
                    "violation_type": result["label"],
                    "confidence": result["confidence"],
                    "bbox": result["bbox"]
                })

    # 保存到 CSV
    df = pd.DataFrame(all_violations)
    df.to_csv(output_csv, index=False, encoding='utf-8')
    print(f"✅ 批量檢測完成，結果已保存到 {output_csv}")

if __name__ == "__main__":
    test_image_path = "/home/ntc/dino/工安管理/ai-new/data/images/186510343_1816338865193347_2587363028274937400_n.jpg"

    print(f"🚀 開始檢測影像：{test_image_path}")
    try:
        results = analyze_image(test_image_path)
        print("✅ 檢測結果如下：")
        for result in results:
            print(f"類別：{result['label']}, 信心：{result['confidence']:.2f}, 邊界框：{result['bbox']}")
    except Exception as e:
        print(f"❌ 發生錯誤：{e}")
