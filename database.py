import sqlite3

def create_connection():
    """建立與資料庫的連線"""
    conn = sqlite3.connect('study_data.db')
    return conn

def init_db():
    """初始化資料庫：建立資料表"""
    conn = create_connection()
    cursor = conn.cursor()
    # 建立表格的 SQL 語句
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            subject TEXT NOT NULL,
            duration REAL NOT NULL,
            rating INTEGER NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def add_record(date, subject, duration, rating):
    """新增一筆紀錄"""
    conn = create_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO records (date, subject, duration, rating)
        VALUES (?, ?, ?, ?)
    ''', (date, subject, duration, rating))
    conn.commit()
    conn.close()

def get_all_records():
    """取得所有紀錄"""
    conn = create_connection()
    # 直接用 pandas 讀取 SQL 查詢結果，超方便！
    import pandas as pd
    df = pd.read_sql_query("SELECT * FROM records", conn)
    conn.close()
    return df