import streamlit as st
import requests
import json

# --- 這裡維持您原本複製的「網頁應用程式網址」 ---
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbz74A4qBbxvkJ6BMT5_qt2-ghr6Lp8KcaKnMevoticZtsFGms9Sr7NvtgQ-s8IM9WVaTA/exec"

st.set_page_config(page_title="期末互評系統 - 單組提交版", layout="centered")
st.title("🎓 期末專案互評系統")

# --- 側邊欄：個人資料（填一次即可） ---
with st.sidebar:
    st.header("1. 身份驗證")
    name = st.text_input("您的姓名")
    sid = st.text_input("您的學號")
    groups = ['第1組', '第2組', '第3組', '第4組(含原10組)', '第5組', '第6組', '第7組', '第8組', '第9組', '第11組', '第12組', '第13組', '第14組', '第15組', '第16組']
    my_group = st.selectbox("您所屬組別", ["請選擇"] + groups)
    
    st.divider()
    st.caption("提示：左側個資填妥後，即可在右側逐一為各組評分。每評完一組請按一次提交。")

# --- 主畫面：逐組評分 ---
if my_group != "請選擇" and name and sid:
    # 過濾掉自己的組別
    other_groups = [g for g in groups if g != my_group]
    
    st.subheader("2. 選擇受評對象")
    target = st.selectbox("您現在要評分哪一組？", ["請選擇組別"] + other_groups)

    if target != "請選擇組別":
        st.write(f"---")
        st.info(f"正在為 **{target}** 進行評分")
        
        # 評分項目
        s1 = st.slider(f"整合性創新", 1, 10, 5, key=f"s1_{target}")
        s2 = st.slider(f"用戶期待", 1, 10, 5, key=f"s2_{target}")
        s3 = st.slider(f"商業存續性", 1, 10, 5, key=f"s3_{target}")
        s4 = st.slider(f"技術可行性", 1, 10, 5, key=f"s4_{target}")
        comment = st.text_input(f"給 {target} 的具體建議", key=f"c_{target}")

        if st.button(f"提交對 {target} 的評分"):
            with st.spinner('正在傳送資料...'):
                try:
                    # 整理成 Apps Script 需要的格式 (單列資料也要包在 list 裡面)
                    single_row_data = [[name, sid, my_group, target, s1, s2, s3, s4, comment]]
                    
                    response = requests.post(WEB_APP_URL, data=json.dumps(single_row_data))
                    
                    if response.text == "Success":
                        st.success(f"✅ {target} 的評分已成功提交！")
                        st.balloons()
                        st.write("請從上方選單選擇下一組繼續評分。")
                    else:
                        st.error("傳送失敗，請確認網路連線。")
                except Exception as e:
                    st.error(f"連線失敗：{str(e)}")
else:
    st.warning("請先於左側選單完整填寫姓名、學號與所屬組別。")
