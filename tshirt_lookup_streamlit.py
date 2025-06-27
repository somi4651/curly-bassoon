import streamlit as st
import pandas as pd

st.title("🧾 수련회 티셔츠 & 참석 정보 조회")

# 고정된 엑셀 파일을 GitHub에 저장해두고 경로를 지정
EXCEL_FILE_URL = "https://raw.githubusercontent.com/somi4651/curly-bassoon/main/data.xlsx"  # 예시 경로

@st.cache_data
def load_data():
    df = pd.read_excel(EXCEL_FILE_URL)
    df.columns = df.columns.str.strip()

    def make_attendance_text(row):
        base = str(row.get('참석여부', '')).strip()
        detail = str(row.get('상세 참석여부', '')).strip()
        if base == '부분참' and detail and detail.lower() != 'nan':
            return f"{base} ({detail})"
        else:
            return base

    df['참석 정보'] = df.apply(make_attendance_text, axis=1)
    return df

df = load_data()

name_query = st.text_input("🔍 이름을 입력하세요 (예: 이다솜(39))")

if name_query:
    result = df[df['이름'].str.contains(name_query, na=False)]
    if not result.empty:
        st.success(f"🔎 {len(result)}건의 결과가 검색되었습니다.")
        st.dataframe(result[['이름', '티셔츠 사이즈', '참석 정보']])
    else:
        st.warning("❌ 해당 이름을 찾을 수 없습니다.")
