import streamlit as st
import pandas as pd

# 🔐 1단계: 비밀번호 인증
PASSWORD = "0710"  # 원하는 비밀번호 4자리로 바꿔도 됨
password_input = st.text_input("🔒 비밀번호 4자리를 입력하세요", type="password")
if password_input != PASSWORD:
    st.warning("비밀번호가 일치하지 않습니다.")
    st.stop()

st.title("🧾 수련회 티셔츠 & 참석 정보 조회")

# 🔽 GitHub에 고정된 경로의 엑셀 파일 불러오기
EXCEL_FILE = "https://raw.githubusercontent.com/somi4651/curly-bassoon/main/data/tshirt_info_2025.xlsx"

# ⏳ 캐시된 데이터 로딩 함수
@st.cache_data
def load_data():
    df = pd.read_excel(EXCEL_FILE)
    df.columns = df.columns.str.strip()
    df['참석 정보'] = df.apply(make_attendance_text, axis=1)
    return df

# 참석 정보 텍스트 포맷팅
def make_attendance_text(row):
    base = str(row.get('참석여부', '')).strip()
    detail = str(row.get('상세 참석여부', '')).strip()
    if base == '부분참' and detail and detail.lower() != 'nan':
        return f"{base} ({detail})"
    else:
        return base

# 데이터 로딩
df = load_data()

# 🔍 이름 검색
name_query = st.text_input("이름을 입력하세요 (예: 이다솜(39))")

# 검색 결과 표시
if name_query:
    result = df[df['이름'].str.contains(name_query, na=False)]
    if not result.empty:
        st.success(f"🔎 {len(result)}건의 결과가 검색되었습니다.")
        # 다운로드 방지: to_csv 등으로 저장하거나 다운로드 버튼 없음
        st.dataframe(result[['이름', '티셔츠 사이즈', '참석 정보']])
    else:
        st.warning("❌ 해당 이름을 찾을 수 없습니다.")
