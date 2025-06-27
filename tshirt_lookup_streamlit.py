# tshirt_lookup_streamlit.py
import streamlit as st
import pandas as pd

st.title("🧾 수련회 티셔츠 & 참석 정보 조회")

# 깃허브에 업로드한 엑셀 파일 직접 불러오기
url = "https://raw.githubusercontent.com/somi4651/curly-bassoon/main/data/%EC%88%98%EB%A0%A8%ED%9A%8C%20%ED%8B%B0%EC%85%94%EC%B8%A0%20%EC%82%AC%EC%9D%B4%EC%A6%88%ED%91%9C%202025%20%EC%97%AC%EB%A6%84.xlsx"
df = pd.read_excel(url)
df.columns = df.columns.str.strip()

def make_attendance_text(row):
    base = str(row.get('참석여부', '')).strip()
    detail = str(row.get('상세 참석여부', '')).strip()
    if base == '부분참' and detail and detail.lower() != 'nan':
        return f"{base} ({detail})"
    else:
        return base

df['참석 정보'] = df.apply(make_attendance_text, axis=1)

name_query = st.text_input("🔍 이름을 입력하세요 (예: 이다솜(39))")

if name_query:
    result = df[df['이름'].str.contains(name_query, na=False)]
    if not result.empty:
        st.success(f"🔎 {len(result)}건의 결과가 검색되었습니다.")
        st.dataframe(result[['이름', '티셔츠 사이즈', '참석 정보']])
    else:
        st.warning("❌ 해당 이름을 찾을 수 없습니다.")
