import streamlit as st
import requests
import json

# --- 這裡填入您剛才複製的「網頁應用程式網址」 ---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbz74A4qBbxvkJ6BMT5_qt2-ghr6Lp8KcaKnMevoticZtsFGms9Sr7NvtgQ-s8IM9WVaTA/exec"

st.set_page_config(page_title="期末互評系統", layout="centered")
st.title("🎓 期末專案互評系統")

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
    st.info(f"您好 {name}，系統已自動為您過濾掉「{my_group}」。")

    all_data = []
    for target in other_groups:
        with st.expander(f"📌 評分對象：{target}"):
            s1 = st.slider(f"{target} - 整合性創新", 1, 10, 5, key=f"s1_{target}")
            s2 = st.slider(f"{target} - 用戶期待", 1, 10, 5, key=f"s2_{target}")
            s3 = st.slider(f"{target} - 商業存續性", 1, 10, 5, key=f"s3_{target}")
            s4 = st.slider(f"{target} - 技術可行性", 1, 10, 5, key=f"s4_{target}")
            comment = st.text_input(f"{target} 的具體建議", key=f"c_{target}")
            # 整理成 Apps Script 需要的一行行格式
            all_data.append([name, sid, my_group, target, s1, s2, s3, s4, comment])

    if st.button("提交所有評分"):
        with st.spinner('正在上傳資料，請稍候...'):
            try:
                # 使用 requests 將資料送往 Google Apps Script
                response = requests.post(WEB_APP_URL, data=json.dumps(all_data))
                
                if response.text == "Success":
                    st.success("✅ 提交成功！資料已安全存入雲端。")
                    st.balloons()
                else:
                    st.error("連線成功但回應異常，請聯繫助教。")
            except Exception as e:
                st.error(f"連線失敗：{str(e)}")
else:
    st.warning("請先於左側選單填寫基本資料。")
