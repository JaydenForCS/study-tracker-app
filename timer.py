import time
import csv # 新增：用來處理 CSV 檔案的工具箱
import os  # 新增：用來跟作業系統互動（例如檢查檔案在不在）
from datetime import datetime

def start_study_session():
    # 1. 獲取科目名稱
    subject = input("請輸入今天要讀的科目: ")
    
    # 2. 開始計時
    print(f"開始紀錄【{subject}】的讀書時間！按下 Enter 鍵結束計時...")
    start_time = datetime.now()
    
    input("計時中... [按 Enter 結束]")
    
    # 3. 結束計時
    end_time = datetime.now()
    duration = end_time - start_time
    minutes_spent = round(duration.total_seconds() / 60, 2)
    
    print(f"讀書結束！你總共讀了 {minutes_spent} 分鐘。")
    
    # 4. 專注度評分
    rating = input("請為這次的專注度評分 (1-5分): ")
    
    # --- 5. 新增的 CSV 存檔功能 ---
    file_name = "study_records.csv" # 定義檔案名稱
    
    # 檢查檔案是否已經存在 (如果不存在，代表是我們第一次存檔)
    file_exists = os.path.isfile(file_name) 
    
    # 打開檔案準備寫入 ('a' 代表 append，也就是接在舊資料下方寫入)
    # encoding='utf-8' 是為了確保中文字不會變成亂碼
    with open(file_name, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        
        # 如果是第一次建立這個檔案，我們先寫入「表頭」(標題列)
        if not file_exists:
            writer.writerow(["Date", "Subject", "Duration_Minutes", "Rating"])
        
        # 準備要存入的資料格式，並寫入檔案
        record_date = start_time.strftime('%Y-%m-%d %H:%M')
        writer.writerow([record_date, subject, minutes_spent, rating])
        
    print(f"\n✅ 太棒了！本次紀錄已成功存入 {file_name} 中！")

if __name__ == "__main__":
    start_study_session()