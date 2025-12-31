import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- 1. 確保網址正確且不含中文字元 ---
# 請務必將下方的網址替換為您正確的 Google Sheet 網址
SHEET_URL = "https://docs.google.com/spreadsheets/d/1nWfDI8Rr1zL5UCiLnWgKW5SWVRHSfFE5w3o9xfG6TqU/edit?usp=sharing"

st.set_page_config(page_title="期末互評系統", layout="centered")
st.title("🎓 期末專案互評系統")

# 建立連線
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 側邊欄 ---
with st.sidebar:
    st.header("身份驗證")
    name = st.text_input("您的姓名")
    sid = st.text_input("您的學號")
    groups = ['第1組', '第2組', '第3組', '第4組(含原10組)', '第5組', '第6組', '第7組', '第8組', '第9組', '第11組', '第12組', '第13組', '第14組', '第15組', '第16組']
    my_group = st.selectbox("您所屬組別", ["請選擇"] + groups)

# --- 主畫面 ---
if my_group != "請選擇" and name and sid:
    other_groups = [g for g in groups if g != my_group]
    st.info(f"您好 {name}，系統已為您隱藏 {my_group}，請開始評分。")

    all_data = []
    for target in other_groups:
        with st.expander(f"📌 評分對象：{target}"):
            s1 = st.slider(f"{target} - 整合性創新", 1, 10, 5, key=f"s1_{target}")
            s2 = st.slider(f"{target} - 用戶期待", 1, 10, 5, key=f"s2_{target}")
            s3 = st.slider(f"{target} - 商業存續性", 1, 10, 5, key=f"s3_{target}")
            s4 = st.slider(f"{target} - 技術可行性", 1, 10, 5, key=f"s4_{target}")
            comment = st.text_input(f"{target} 的建議", key=f"c_{target}")
            # 確保資料為字串格式，避免編碼錯誤
            all_data.append([str(name), str(sid), str(my_group), str(target), s1, s2, s3, s4, str(comment)])

    if st.button("提交所有評分"):
        try:
            # 指定 worksheet="Sheet1" 避開中文標籤名稱問題
            df = conn.read(spreadsheet=SHEET_URL, worksheet="Sheet1")
            
            new_rows = pd.DataFrame(all_data, columns=["姓名", "學號", "所屬組別", "受評組別", "創新", "期待", "存續", "技術", "建議"])
            
            # 使用 pd.concat 組合舊資料與新資料
            updated_df = pd.concat([df, new_rows], ignore_index=True)
            
            # 寫回雲端 (指定寫入 Sheet1)
            conn.update(spreadsheet=SHEET_URL, worksheet="Sheet1", data=updated_df)
            
            st.success("✅ 提交成功！請關閉頁面或通知助教。")
            st.balloons()
        except Exception as e:
            # 這裡會顯示具體的錯誤訊息，方便除錯
            st.error(f"連線失敗：{str(e)}")
else:
    st.warning("請先完整填寫左側個人資料，以啟動評分介面。")
