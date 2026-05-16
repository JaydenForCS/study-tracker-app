# 📚 Study Tracker App (個人讀書追蹤儀表板)

這是一個使用純 Python 與 Streamlit 打造的輕量級網頁應用程式。具備多使用者帳號系統與精美的數據視覺化圖表，幫助你輕鬆掌握自己的學習歷程。

## ✨ 核心功能 (Features)

* **🔐 多使用者帳號系統**：支援註冊與登入功能，使用 Hash 單向加密保護密碼，每個人的讀書紀錄各自獨立、互不干擾。
* **⏱️ 即時讀書計時器**：輸入科目即可開始計時，結束後自動結算時間並存入資料庫。
* **✍️ 手動補登系統**：忘記開計時器也沒關係，支援事後手動輸入讀書紀錄。
* **📊 互動式視覺化儀表板**：
    * 導入 `Plotly` 繪製精美圖表。
    * 提供各科讀書時間總覽（長條圖）與各科時間佔比（甜甜圈圓餅圖）。
    * 支援「今天、最近 7 天、全部時間」動態時間範圍篩選。
* **📝 歷史資料管理**：可直接在網頁上瀏覽與操作專屬的歷史紀錄，並具備自動重新整理功能。

## 🛠️ 技術堆疊 (Tech Stack)

* **前端網頁框架**：[Streamlit](https://streamlit.io/)
* **資料處理與視覺化**：Pandas, Plotly
* **後端資料庫**：SQLite (內建關聯式資料庫)
* **資安加密**：Python `hashlib` (SHA-256)

## 🚀 如何在本地端執行 (How to Run)

1. 將此專案 Clone 到本地端：
   ```bash
   git clone [https://github.com/JaydenForCS/study-tracker-app.git](https://github.com/JaydenForCS/study-tracker-app.git)

2. 進入專案資料夾：
   ```bash
   cd study-tracker-app

3. 安裝所需的 Python 套件：
   ```bash
   pip install -r requirements.txt

4. 啟動 Streamlit 伺服器：
   ```bash
   streamlit run app.py