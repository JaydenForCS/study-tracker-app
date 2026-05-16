import streamlit as st
import pandas as pd
from datetime import datetime
import time

# 確保引入了新版資料庫的所有必備工具
from database import init_db, add_record, get_user_records, create_user, verify_user

# --- 初始化資料庫 ---
init_db()

# --- 1. 網頁基本設定 ---
st.set_page_config(page_title="讀書追蹤 App", page_icon="📚")

# --- 2. 登入狀態管理 (VIP 識別證) ---
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

# --- 3. 判斷畫面要顯示什麼 ---
if not st.session_state.logged_in:
    # ==========================================
    # 畫面 A：尚未登入，顯示大門
    # ==========================================
    st.title("🔐 歡迎來到讀書追蹤 App")
    
    tab1, tab2 = st.tabs(["🔑 登入", "📝 註冊新帳號"])
    
    with tab1:
        st.subheader("登入你的帳號")
        login_user = st.text_input("帳號", key="login_user")
        login_pwd = st.text_input("密碼", type="password", key="login_pwd")
        
        if st.button("登入", use_container_width=True):
            if verify_user(login_user, login_pwd):
                st.session_state.logged_in = True
                st.session_state.username = login_user
                st.success("登入成功！為您準備專屬儀表板中...")
                time.sleep(1)
                st.rerun()
            else:
                st.error("帳號或密碼錯誤，請檢查後再試一次！")
                
    with tab2:
        st.subheader("註冊新帳號")
        reg_user = st.text_input("設定帳號", key="reg_user")
        reg_pwd = st.text_input("設定密碼", type="password", key="reg_pwd")
        
        if st.button("註冊", use_container_width=True):
            if create_user(reg_user, reg_pwd):
                st.success("註冊成功！🎉 請切換到左側「登入」分頁進行登入。")
            else:
                st.error("哎呀！這個帳號已經有人使用囉，請換一個名字吧！")

else:
    # ==========================================
    # 畫面 B：已登入，顯示專屬讀書儀表板
    # ==========================================
    st.title(f"📚 {st.session_state.username} 的專屬讀書追蹤 App")
    
    if st.sidebar.button("🚪 登出系統"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    # --- 這裡開始，全部向右縮排，代表登入後才看得見 ---
    
    # 側邊欄：設定科目與專注度
    st.sidebar.header("📝 這次要讀什麼？")
    subject = st.sidebar.text_input("輸入科目名稱", "程式設計")
    rating = st.sidebar.slider("為這次的專注度評分", 1, 5, 5)

    # 狀態保險箱
    if 'is_running' not in st.session_state:
        st.session_state.is_running = False
        st.session_state.start_time = None

    # 畫面佈局：兩個按鈕
    col1, col2 = st.columns(2)

    with col1:
        if st.button("▶️ 開始讀書", use_container_width=True):
            st.session_state.is_running = True
            st.session_state.start_time = datetime.now()
            st.success(f"開始計時！目前科目：{subject}")

    with col2:
        if st.button("⏹️ 結束並存檔", use_container_width=True):
            if st.session_state.is_running:
                end_time = datetime.now()
                duration = end_time - st.session_state.start_time
                minutes_spent = round(duration.total_seconds() / 60, 2)
                record_date = st.session_state.start_time.strftime('%Y-%m-%d %H:%M')
                
                # 🌟 改用 SQL 的 add_record，並把 username 傳進去
                add_record(st.session_state.username, record_date, subject, minutes_spent, rating)
                
                st.session_state.is_running = False
                st.success(f"辛苦了！本次讀書 {minutes_spent} 分鐘，已成功存檔！圖表更新中...")
                time.sleep(1)
                st.rerun()
            else:
                st.warning("你還沒開始計時喔！")

    # --- 顯示歷史紀錄 ---
    st.divider() 
    st.subheader("📊 歷史讀書紀錄")
    
    # 🌟 改用 SQL 函數，只抓取當前登入者的資料
    df = get_user_records(st.session_state.username)
    
    if not df.empty:
        st.dataframe(df, use_container_width=True)
    else:
        st.info("目前還沒有紀錄，趕快開始你的第一次讀書吧！")

    # --- 數據視覺化 (圖表) ---
    st.divider()
    st.subheader("📈 讀書時間總覽")

    if not df.empty:
        # 注意：欄位名稱改成符合 SQL 設計的小寫 (date, subject, duration, rating)
        df['date'] = pd.to_datetime(df['date'])
        
        time_filter = st.radio("過濾時間範圍：", ["全部時間", "今天", "最近 7 天"], horizontal=True)
        now = pd.Timestamp.now()
        
        if time_filter == "今天":
            filtered_df = df[df['date'].dt.date == now.date()]
        elif time_filter == "最近 7 天":
            seven_days_ago = now - pd.Timedelta(days=7)
            filtered_df = df[df['date'] >= seven_days_ago]
        else:
            filtered_df = df 

        if not filtered_df.empty:
            chart_data = filtered_df.groupby("subject")["duration"].sum()
            st.bar_chart(chart_data)
        else:
            st.info(f"在「{time_filter}」這個範圍內，你還沒有任何讀書紀錄喔！")

    # --- 專注度深度分析 ---
    st.divider()
    st.subheader("🎯 專注度深度分析")

    if not df.empty:
        stat_col1, stat_col2 = st.columns(2)

        with stat_col1:
            st.write("📖 各科平均專注度")
            subject_rating = df.groupby("subject")["rating"].mean()
            st.bar_chart(subject_rating)

        with stat_col2:
            st.write("📅 每日平均專注度")
            daily_rating = df.groupby(df['date'].dt.date)["rating"].mean()
            st.line_chart(daily_rating)

        st.write("⏰ 不同時段專注度分析")
        
        def get_time_period(hour):
            if 5 <= hour < 12: return "🌅 早上 (5-12)"
            elif 12 <= hour < 18: return "☀️ 下午 (12-18)"
            elif 18 <= hour < 24: return "🌙 晚上 (18-24)"
            else: return "🦉 深夜 (0-5)"

        df['Period'] = df['date'].dt.hour.apply(get_time_period)
        period_rating = df.groupby("Period")["rating"].mean()
        st.bar_chart(period_rating)

    # --- 手動補登紀錄 ---
    st.divider()
    st.subheader("✍️ 手動補登紀錄")

    with st.form("manual_entry_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            new_date = st.date_input("日期", pd.Timestamp.now().date())
            new_time = st.time_input("時間", pd.Timestamp.now().time())
            new_subject = st.text_input("科目", "物理")
            
        with col2:
            new_duration = st.number_input("讀書時長 (分鐘)", min_value=1, value=60)
            new_rating = st.slider("專注度評分 (補登)", 1, 5, 4)
            
        submit_button = st.form_submit_button("💾 儲存補登紀錄", use_container_width=True)
        
        if submit_button:
            datetime_str = f"{new_date} {new_time.strftime('%H:%M')}"
            
            # 🌟 加上 username 參數，並傳入手動輸入的值
            add_record(st.session_state.username, datetime_str, new_subject, new_duration, new_rating)
                
            st.success("✅ 補登成功！圖表更新中...")
            time.sleep(1)
            st.rerun()