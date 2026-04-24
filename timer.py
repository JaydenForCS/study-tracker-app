import time
from datetime import datetime

def start_study_session():
    # 1. 獲取科目名稱
    subject = input("請輸入今天要讀的科目: ")
    
    # 2. 開始計時
    print(f"開始紀錄【{subject}】的讀書時間！按下 Enter 鍵結束計時...")
    start_time = datetime.now() # 紀錄開始的精確時間
    
    input("計時中... [按 Enter 結束]") # 程式會停在這裡等使用者
    
    # 3. 結束計時
    end_time = datetime.now()
    duration = end_time - start_time # 計算時間差
    
    # 將時間差轉換為分鐘 (四捨五入到小數點後兩位)
    minutes_spent = round(duration.total_seconds() / 60, 2)
    
    print(f"讀書結束！你總共讀了 {minutes_spent} 分鐘。")
    
    # 4. 專注度評分
    rating = input("請為這次的專注度評分 (1-5分): ")
    
    # 5. 顯示結果 (下一階段我們再來寫存檔功能)
    print(f"\n--- 本次紀錄 ---")
    print(f"時間: {start_time.strftime('%Y-%m-%d %H:%M')}")
    print(f"科目: {subject}")
    print(f"時長: {minutes_spent} 分鐘")
    print(f"專注度: {rating}/5")

if __name__ == "__main__":
    start_study_session()