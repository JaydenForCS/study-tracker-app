import streamlit as st
import pandas as pd
from datetime import datetime
import csv
import os

# --- 1. 網頁基本設定 ---
st.set_page_config(page_title="讀書追蹤 App", page_icon="📚")
st.title("📚 我的專屬讀書追蹤 App")

# --- 2. 側邊欄：設定科目與專注度 ---
st.sidebar.header("📝 這次要讀什麼？")
subject = st.sidebar.text_input("輸入科目名稱", "程式設計")
rating = st.sidebar.slider("為這次的專注度評分", 1, 5, 5)

# --- 3. 金魚腦的記憶保險箱 (Session State) ---
# 幫網頁記住「是不是正在計時」以及「開始的時間」
if 'is_running' not in st.session_state:
    st.session_state.is_running = False
    st.session_state.start_time = None

# --- 4. 畫面佈局：兩個按鈕 ---
col1, col2 = st.columns(2) # 把畫面切成左右兩半

with col1:
    # 開始按鈕
    if st.button("▶️ 開始讀書", use_container_width=True):
        st.session_state.is_running = True
        st.session_state.start_time = datetime.now() # 記下當下時間
        st.success(f"開始計時！目前科目：{subject}")

with col2:
    # 結束按鈕
    if st.button("⏹️ 結束並存檔", use_container_width=True):
        if st.session_state.is_running: # 確保有先按過開始
            end_time = datetime.now()
            duration = end_time - st.session_state.start_time
            minutes_spent = round(duration.total_seconds() / 60, 2)
            
            # --- 這是我們上一課寫的存檔邏輯 ---
            file_name = "study_records.csv"
            file_exists = os.path.isfile(file_name)
            with open(file_name, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(["Date", "Subject", "Duration_Minutes", "Rating"])
                record_date = st.session_state.start_time.strftime('%Y-%m-%d %H:%M')
                writer.writerow([record_date, subject, minutes_spent, rating])
            
            # 存檔完畢，把計時狀態歸零
            st.session_state.is_running = False
            st.success(f"辛苦了！本次讀書 {minutes_spent} 分鐘，已成功存檔！")
        else:
            st.warning("你還沒開始計時喔！")

# --- 5. 顯示歷史紀錄 ---
st.divider() # 畫一條分隔線
st.subheader("📊 歷史讀書紀錄")

file_name = "study_records.csv"
if os.path.isfile(file_name):
    # 使用 Pandas 讀取 CSV，並用 Streamlit 顯示成精美表格
    df = pd.read_csv(file_name)
    st.dataframe(df, use_container_width=True)
else:
    st.info("目前還沒有紀錄，趕快開始你的第一次讀書吧！")