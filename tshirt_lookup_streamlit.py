import streamlit as st
import pandas as pd
from datetime import datetime

# ✅ 설정
PASSWORD = "0710"
EXCEL_URL = "https://raw.githubusercontent.com/somi4651/curly-bassoon/main/data/tshirt_info_2025.xlsx"

# ✅ 페이지 기본 설정
st.set_page_config(page_title="수련회 티셔츠 & 참석 정보 조회", layout="wide")
st.title("🧾 수련회 티셔츠 & 참석 정보 조회")

# ✅ 비밀번호 입력
password_input = st.text_input("🔐 비밀번호 4자리를 입력하세요", type="password")
if password_input != PASSWORD:
    st.warning("비밀번호가 일치하지 않습니다.")
    st.stop()

# ✅ 안내문
st.info("✅ 개인정보 보호를 위해 본인 신청 확인 용도로만 사용 부탁드립니다.")

# ✅ 엑셀 데이터 불러오기
@st.cache_data(ttl=600)
def load_data():
    return pd.read_excel(EXCEL_URL)

df = load_data()

# ✅ 이름 검색
name = st.text_input("이름을 입력하세요 (예: 이다솜(39))").strip()

if name:
    result = df[df['이름'].str.contains(name, na=False)]

    if not result.empty:
        # ✅ 로그 저장
        with open("조회로그.txt", "a", encoding="utf-8") as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] 조회: {name}\n")

        st.success(f"🔍 {len(result)}건의 결과가 검색되었습니다.")

        # ✅ 표시할 컬럼만 추출 + 컬럼명 축약
        result_display = result[['이름', '티셔츠 사이즈', '참석 정보']].copy()
        result_display.columns = ['이름', '사이즈', '참석']

        # ✅ 인덱스 숨기고 넓게 표시
        st.dataframe(result_display.reset_index(drop=True), use_container_width=True)
    else:
        st.error("검색 결과가 없습니다. 이름을 다시 확인해주세요.")
