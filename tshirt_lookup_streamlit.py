import streamlit as st
import pandas as pd

# 🔐 4자리 비밀번호 설정
CORRECT_PASSWORD = "0710"

# 타이틀
st.title("🧾 수련회 티셔츠 & 참석 정보 조회")

# 1️⃣ 비밀번호 입력
password_input = st.text_input("🔒 비밀번호 4자리를 입력하세요", type="password")

if password_input == CORRECT_PASSWORD:
    st.success("✅ 인증되었습니다. 조회를 시작하세요!")

    # 2️⃣ GitHub에 고정된 파일 경로에서 불러오기 (업로드 없이 고정된 파일만 사용)
    EXCEL_FILE = "data/수련회 티셔츠 사이즈표 2025 여름.xlsx"

    @st.cache_data
    def load_data():
        df = pd.read_excel(EXCEL_FILE)
        df.columns = df.columns.str.strip()
        df['참석 정보'] = df.apply(make_attendance_text, axis=1)
        return df

    def make_attendance_text(row):
        base = str(row.get('참석여부', '')).strip()
        detail = str(row.get('상세 참석여부', '')).strip()
        if base == '부분참' and detail and detail.lower() != 'nan':
            return f"{base} ({detail})"
        else:
            return base

    df = load_data()

    # 3️⃣ 이름 입력 후 조회
    name_query = st.text_input("🔍 이름을 입력하세요 (예: 이다솜(39))")
    if name_query:
        result = df[df['이름'].str.contains(name_query, na=False)]
        if not result.empty:
            st.success(f"🔎 {len(result)}건의 결과가 검색되었습니다.")
            st.dataframe(result[['이름', '티셔츠 사이즈', '참석 정보']], use_container_width=True)
        else:
            st.warning("❌ 해당 이름을 찾을 수 없습니다.")
else:
    if password_input:
        st.error("❌ 비밀번호가 틀렸습니다. 다시 시도해주세요.")
