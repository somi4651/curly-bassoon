import streamlit as st
import pandas as pd

# 앱 제목
st.set_page_config(page_title="수련회 티셔츠 & 참석 정보 조회", layout="centered")
st.markdown("## 🧾 수련회 티셔츠 & 참석 정보 조회")

# 비밀번호 입력
password = st.text_input("🔐 비밀번호 4자리를 입력하세요", type="password")
if password != "0710":
    st.warning("비밀번호가 올바르지 않습니다.")
    st.stop()

# 데이터 불러오기
@st.cache_data
def load_data():
    df = pd.read_excel("tshirt_info_2025.xlsx")
    df = df[["이름", "티셔츠 사이즈", "참석여부"]]
    df.columns = ["이름", "사이즈", "참석 정보"]
    return df

df = load_data()

# 이름 검색창
name_input = st.text_input("🔍 이름을 입력하세요 (예: 이다솜)")

if name_input:
    result = df[df["이름"].str.contains(name_input.strip())]

    if not result.empty:
        st.success(f"🔍 {len(result)}건의 결과가 검색되었습니다.")
        # ✅ 인덱스 없이, 테이블형식으로 깔끔하게 출력
        st.table(result)
    else:
        st.error("일치하는 결과가 없습니다. 철자나 괄호 포함 여부를 다시 확인해주세요.")

# 안내 메시지
st.markdown("---")
st.info("📌 개인정보 보호를 위해 본인 신청 확인 용도로만 사용 부탁드립니다.")
