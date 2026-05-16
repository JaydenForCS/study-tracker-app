import sqlite3
import hashlib # 新增：用來進行密碼加密的工具
import pandas as pd

def create_connection():
    return sqlite3.connect('study_data.db')

# database.py 的局部修改

def init_db():
    conn = create_connection()
    cursor = conn.cursor()
    
    # 建立使用者表格 (維持不變)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL
        )
    ''')
    
    # 建立紀錄表格 (移除 rating 欄位)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            date TEXT NOT NULL,
            subject TEXT NOT NULL,
            duration REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# 新增紀錄 (移除 rating 參數)
def add_record(username, date, subject, duration):
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO records (username, date, subject, duration)
        VALUES (?, ?, ?, ?)
    ''', (username, date, subject, duration))
    conn.commit()
    conn.close()

# --- 密碼處理邏輯 ---
def make_hash(password):
    """將密碼轉換為 Hash 亂碼"""
    return hashlib.sha256(str.encode(password)).hexdigest()

def create_user(username, password):
    """註冊新帳號"""
    conn = create_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password_hash) VALUES (?, ?)', 
                       (username, make_hash(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        # 如果帳號已經存在，會觸發這個錯誤
        return False
    finally:
        conn.close()

def verify_user(username, password):
    """驗證登入密碼"""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT password_hash FROM users WHERE username = ?', (username,))
    result = cursor.fetchone()
    conn.close()
    
    # 如果有找到帳號，且輸入的密碼 Hash 後與資料庫相符
    if result and result[0] == make_hash(password):
        return True
    return False

def get_user_records(username):
    """只取得特定使用者的紀錄"""
    conn = create_connection()
    df = pd.read_sql_query("SELECT * FROM records WHERE username = ?", conn, params=(username,))
    conn.close()
    return df