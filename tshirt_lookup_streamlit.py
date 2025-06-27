import streamlit as st
import pandas as pd
from datetime import datetime

# 🔒 비밀번호 4자리 설정
PASSWORD = "2580"

# 📁 엑셀 파일 불러오기 (raw 파일 링크)
EXCEL_URL = "https://raw.githubusercontent.com/somi4651/curly-bassoon/main/data/tshirt_info_2025.xlsx"

# 📜 앱 제목
st.set_page_config(page_title="수련회 티셔츠 & 참석 정보 조회", layout="centered")
st.title("🧾 수련회 티셔츠 & 참석 정보 조회")

# 🔐 비밀번호 입력
password_input = st.text_input("🔐 비밀번호 4자리를 입력하세요", type="password")
if password_input != PASSWORD:
    st.warning("비밀번호가 일치하지 않습니다.")
    st.stop()

# 🔒 안내 문구
st.info("✅ 개인정보 보호를 위해 본인 신청 확인 용도로만 사용 부탁드립니다.")

# 📄 데이터 불러오기
@st.cache_data(ttl=600)
def load_data():
    df = pd.read_excel(EXCEL_URL)
    return df

data = load_data()

# 🔍 이름 입력
name_query = st.text_input("이름을 입력하세요 (예: 이다솜(39))")

if name_query:
    result_df = data[data['이름'].str.contains(name_query.strip(), na=False)]

    if not result_df.empty:
        # ✅ 로그 저장
        with open("조회로그.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 조회: {name_query}\n")

        st.success(f"🔍 {len(result_df)}건의 결과가 검색되었습니다.")

        # 📱 모바일 최적화를 위한 열 선택 및 축약
        result_df_display = result_df[['이름', '티셔츠 사이즈', '참석 정보']].copy()
        result_df_display.columns = ['이름', '사이즈', '참석']
        st.dataframe(result_df_display, use_container_width=True, hide_index=True)
    else:
        st.error("검색 결과가 없습니다. 이름을 정확히 입력해주세요.")
