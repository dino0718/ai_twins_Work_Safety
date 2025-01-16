import sys
import os
import torch
import cv2
import csv
from datetime import datetime
from pathlib import Path

# 添加 YOLOv5 文件夾到 Python 搜索路徑
YOLOV5_PATH = os.path.join(os.path.dirname(__file__), 'yolov5')
sys.path.append(YOLOV5_PATH)


from yolov5.models.common import DetectMultiBackend
from yolov5.utils.general import non_max_suppression, scale_boxes, xyxy2xywh
from yolov5.utils.torch_utils import select_device

# 添加 YOLOv5 文件夾到 Python 搜索路徑
YOLOV5_PATH = os.path.join(os.path.dirname(__file__), 'yolov5')
sys.path.append(YOLOV5_PATH)

# 模型路徑
MODEL_PATH = "/home/ntc/dino/工安管理/ai-new/models/best_teacher.pt"

# 初始化 YOLO 模型
device = select_device('cpu')  # 替換為 'cuda:0' 使用 GPU
model = DetectMultiBackend(MODEL_PATH, device=device)

print(f"✅ 成功加載模型：{MODEL_PATH}")

def analyze_image(image_path, conf_thres=0.25, iou_thres=0.45):
    """
    使用 YOLO 模型檢測單張影像，並返回檢測結果。
    """
    # 加載影像
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError(f"無法加載影像：{image_path}")
    img0 = img.copy()  # 保存原始影像
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # 轉為 RGB 格式

    # 確保影像大小符合 YOLO 的要求
    img = cv2.resize(img, (640, 640))  # 調整為 640x640 的大小

    # 將影像轉換為 PyTorch 張量
    img = torch.from_numpy(img).permute(2, 0, 1).float().to(device)  # [H, W, C] -> [C, H, W]
    img = img.unsqueeze(0)  # 增加 batch 維度
    img /= 255.0  # 歸一化到 [0, 1]

    # 推論
    pred = model(img)
    pred = non_max_suppression(pred, conf_thres, iou_thres)

    # 處理檢測結果
    results = []
    for det in pred:
        if det is not None and len(det):
            det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], img0.shape).round()
            for *xyxy, conf, cls in det:
                results.append({
                    "class": model.names[int(cls)],
                    "confidence": float(conf),
                    "xmin": int(xyxy[0]),
                    "ymin": int(xyxy[1]),
                    "xmax": int(xyxy[2]),
                    "ymax": int(xyxy[3])
                })
    return results

def batch_analyze_images(input_dir, output_csv, conf_thres=0.25, iou_thres=0.45):
    """
    批量檢測目錄中的所有影像，並將結果保存到 CSV 文件。
    """
    input_path = Path(input_dir)
    if not input_path.exists() or not input_path.is_dir():
        raise ValueError(f"輸入目錄不存在：{input_dir}")

    # 創建輸出 CSV 文件
    with open(output_csv, mode="w", newline="") as csvfile:
        fieldnames = ["image_name", "class", "confidence", "xmin", "ymin", "xmax", "ymax", "timestamp"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # 遍歷目錄中的影像
        image_files = [f for f in input_path.iterdir() if f.suffix.lower() in [".jpg", ".jpeg", ".png"]]
        if not image_files:
            raise ValueError(f"目錄中沒有找到影像文件：{input_dir}")

        print(f"🚀 開始檢測目錄：{input_dir}，共 {len(image_files)} 張影像")
        for image_file in image_files:
            print(f"🔍 檢測影像：{image_file}")
            try:
                results = analyze_image(image_file, conf_thres, iou_thres)
                for result in results:
                    writer.writerow({
                        "image_name": image_file.name,
                        "class": result["class"],
                        "confidence": result["confidence"],
                        "xmin": result["xmin"],
                        "ymin": result["ymin"],
                        "xmax": result["xmax"],
                        "ymax": result["ymax"],
                        "timestamp": datetime.now().isoformat()
                    })
            except Exception as e:
                print(f"❌ 檢測過程發生錯誤：{image_file}, 錯誤信息：{e}")


if __name__ == "__main__":
    # 測試目錄路徑
    input_dir = "/home/ntc/dino/工安管理/ai-new/data/images"  # 修改為您的影像目錄路徑
    output_csv = "/home/ntc/dino/工安管理/ai-new/data/results.csv"  # 保存檢測結果的 CSV 文件

    try:
        batch_analyze_images(input_dir, output_csv, conf_thres=0.25, iou_thres=0.45)
        print(f"✅ 批量檢測完成，結果已保存到：{output_csv}")
    except Exception as e:
        print(f"❌ 批量檢測過程發生錯誤：{e}")
