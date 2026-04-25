# 📚 Study Tracker App (個人讀書追蹤儀表板)

這是一個使用純 Python 與 Streamlit 打造的輕量級網頁應用程式。旨在幫助使用者紀錄讀書時間、評估專注度，並透過數據視覺化圖表，輕鬆掌握自己的學習歷程。

## ✨ 核心功能 (Features)

* **⏱️ 即時讀書計時器**：輸入科目即可開始計時，結束後自動結算時間並評分。
* **✍️ 手動補登系統**：忘記開計時器也沒關係，支援事後補登讀書紀錄。
* **📊 數據視覺化儀表板**：
    * 各科讀書時間總覽（長條圖）
    * 每日/各科平均專注度趨勢分析（折線圖）
    * 支援「今天、最近 7 天、全部時間」等動態時間範圍篩選。
* **📝 互動式資料管理 (CRUD)**：可直接在網頁上修改或刪除錯誤的歷史紀錄，並具備自動重新整理功能。

## 🛠️ 技術堆疊 (Tech Stack)

* **前端介面**：Streamlit
* **資料處理與視覺化**：Pandas
* **資料儲存**：CSV (本機儲存)

## 🚀 如何在本地端執行 (How to Run)

1. 將此專案 Clone 到本地端：
   ```bash
   git clone [https://github.com/JaydenForCS/study-tracker-app](https://github.com/JaydenForCS/study-tracker-app)