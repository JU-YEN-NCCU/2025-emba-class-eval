import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 這裡換成您的 Google Sheets 網址 (確認權限為「知道連結的人均可編輯」)
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
            all_data.append([name, sid, my_group, target, s1, s2, s3, s4, comment])

    if st.button("提交所有評分"):
        try:
            # 讀取現有資料 (若試算表全空會報錯，請至少先在第一行手動輸入標題)
            df = conn.read(spreadsheet=SHEET_URL)
            new_rows = pd.DataFrame(all_data, columns=["姓名", "學號", "所屬組別", "受評組別", "創新", "期待", "存續", "技術", "建議"])
            updated_df = pd.concat([df, new_rows], ignore_index=True)
            conn.update(spreadsheet=SHEET_URL, data=updated_df)
            st.success("✅ 提交成功！")
            st.balloons()
        except Exception as e:
            st.error(f"連線失敗：{e}")
else:
    st.warning("請先填寫左側個人資料。")
