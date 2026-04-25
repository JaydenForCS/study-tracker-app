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

# --- 6. 數據視覺化 (圖表) ---
st.divider()
st.subheader("📈 讀書時間總覽")

if os.path.isfile(file_name):
    df = pd.read_csv(file_name)
    
    if not df.empty:
        # 🌟 步驟 1: 將 Date 欄位從「純文字」轉換為電腦懂的「時間格式」
        df['Date'] = pd.to_datetime(df['Date'])
        
        # 🌟 步驟 2: 在網頁上建立一個按鈕選單 (Radio button)
        time_filter = st.radio("過濾時間範圍：", ["全部時間", "今天", "最近 7 天"], horizontal=True)
        
        # 取得現在的精確時間
        now = pd.Timestamp.now()
        
        # 🌟 步驟 3: 根據使用者的選擇，篩選資料 (Data Filtering)
        if time_filter == "今天":
            # 條件：只保留「日期」等於「今天日期」的資料
            filtered_df = df[df['Date'].dt.date == now.date()]
            
        elif time_filter == "最近 7 天":
            # 條件：只保留大於等於「7天前」的資料
            seven_days_ago = now - pd.Timedelta(days=7)
            filtered_df = df[df['Date'] >= seven_days_ago]
            
        else:
            # 全部時間：不做任何篩選
            filtered_df = df 

        # 🌟 步驟 4: 把篩選過後的資料畫成圖表
        if not filtered_df.empty:
            chart_data = filtered_df.groupby("Subject")["Duration_Minutes"].sum()
            st.bar_chart(chart_data)
        else:
            # 如果那個時間段沒有資料，給予溫馨提示
            st.info(f"在「{time_filter}」這個範圍內，你還沒有任何讀書紀錄喔！趕快去讀書吧！")

# --- 7. 專注度深度分析 ---
st.divider()
st.subheader("🎯 專注度深度分析")

if os.path.isfile(file_name) and not df.empty:
    # 這裡我們用剛才已經轉換過時間格式的 df 繼續操作
    
    # 建立三欄式佈局來放三種不同的數據
    stat_col1, stat_col2 = st.columns(2)

    with stat_col1:
        st.write("📖 各科平均專注度")
        # 依科目分組，計算評分平均值
        subject_rating = df.groupby("Subject")["Rating"].mean()
        st.bar_chart(subject_rating)

    with stat_col2:
        st.write("📅 每日平均專注度")
        # 依日期 (不含時間) 分組，計算評分平均值
        daily_rating = df.groupby(df['Date'].dt.date)["Rating"].mean()
        st.line_chart(daily_rating) # 每日趨勢用折線圖比較好看

    # --- 不同時間段的專注度分析 ---
    st.write("⏰ 不同時段專注度分析")
    
    # 定義一個簡單的函數來判斷時段
    def get_time_period(hour):
        if 5 <= hour < 12: return "🌅 早上 (5-12)"
        elif 12 <= hour < 18: return "☀️ 下午 (12-18)"
        elif 18 <= hour < 24: return "🌙 晚上 (18-24)"
        else: return "🦉 深夜 (0-5)"

    # 創造一個新欄位「時段」
    df['Period'] = df['Date'].dt.hour.apply(get_time_period)
    
    # 依照時段分組計算平均專注度
    period_rating = df.groupby("Period")["Rating"].mean()
    
    # 顯示數據
    st.bar_chart(period_rating)