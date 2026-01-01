import streamlit as st
import requests
import json

# --- 這裡請維持您原本的 Apps Script 網址 ---
WEB_APP_URL = "https://script.google.com/macros/library/d/11egfvTY7y5Mif8i2NefD5momRkCYuaceO0z6U4_Gz-1Q1-EVnYt4_UBA/2"

st.set_page_config(page_title="期末互評系統", layout="centered")
st.title("🎓 期末專案互評系統")

# --- 側邊欄：個人資料 ---
with st.sidebar:
    st.header("1. 身份驗證")
    name = st.text_input("您的姓名")
    sid = st.text_input("您的學號")
    groups = ['第1組', '第2組', '第3組', '第4組(含原10組)', '第5組', '第6組', '第7組', '第8組', '第9組', '第11組', '第12組', '第13組', '第14組', '第15組', '第16組']
    my_group = st.selectbox("您所屬組別", ["請選擇"] + groups)
    st.divider()
    st.caption("填寫指南：選好受評對象後，評完兩項並按提交即可。")

# --- 主畫面：逐組評分 ---
if my_group != "請選擇" and name and sid:
    other_groups = [g for g in groups if g != my_group]
    
    st.subheader("2. 選擇受評對象")
    target = st.selectbox("您現在要評分哪一組？", ["請選擇組別"] + other_groups)

    if target != "請選擇組別":
        st.write(f"---")
        st.info(f"正在為 **{target}** 進行評分")
        
        # 項目 1：整合性創新
        st.markdown("### 1. 整合性創新 Innovation")
        st.caption("評分參考：a.發想階段夠多Out of box ideas；b.平衡需求/商業/技術之方案；c.建立生態圈可能性。")
        s1 = st.slider("評分 (1-10分)", 1, 10, 5, key=f"s1_{target}")

        st.write("") # 間隔

        # 項目 2：綜合評分 (DVF)
        st.markdown("### 2. 綜合評分 (D/V/F)")
        st.caption("評分參考：\n"
                   "- 用戶期待(D)：定義洞見、解決顯/隱性需求、驗證需求。\n"
                   "- 商業存續(V)：供應鏈策略、市場導入評估、成本預算計畫。\n"
                   "- 技術可行(F)：原型測試發現錯誤、開發支撐量產、技術藍圖。")
        s2 = st.slider("評分 (1-10分)", 1, 10, 5, key=f"s2_{target}")

        st.write("") # 間隔

        # 項目 3：整體建議
        st.markdown("### 3. 整體建議")
        comment = st.text_area("若有具體建議請填寫（非必填）", placeholder="請輸入對該組的建議...", key=f"c_{target}")

        # 項目 4：老師要求的備註文字
        st.warning("【備註：上列項目僅做為評審與分享團隊互動討論時的參考項目，實際評分仍需視各專案情境，給予綜合性的分數。】")

        if st.button(f"確認提交對 {target} 的評分"):
            with st.spinner('正在上傳至雲端試算表...'):
                try:
                    # 資料打包（對應 Google Sheet 的 7 個欄位）
                    single_row_data = [[name, sid, my_group, target, s1, s2, comment]]
                    
                    response = requests.post(WEB_APP_URL, data=json.dumps(single_row_data))
                    
                    if response.text == "Success":
                        st.success(f"✅ {target} 評分成功！")
                        st.balloons()
                    else:
                        st.error("連線成功但寫入失敗，請聯繫助教。")
                except Exception as e:
                    st.error(f"連線失敗：{str(e)}")
else:
    st.warning("請先於左側填寫個人資料以開始評分。")
