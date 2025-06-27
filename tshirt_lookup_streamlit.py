import streamlit as st
import pandas as pd
from datetime import datetime
import os

# 📌 GitHub에 고정 업로드된 엑셀 파일 경로
EXCEL_FILE = "https://raw.githubusercontent.com/somi4651/curly-bassoon/main/data/tshirt_info_2025.xlsx"

# ✅ 비밀번호 인증
password_input = st.text_input("🔐 비밀번호 4자리를 입력하세요", type="password")
if password_input != "0710":  # 🔒 비밀번호 변경 가능
    st.warning("인증된 사용자만 접근할 수 있습니다.")
    st.stop()

# ✅ 엑셀 데이터 로딩
@st.cache_data
def load_data():
    df = pd.read_excel(EXCEL_FILE)
    df.columns = df.columns.str.strip()
    df['참석 정보'] = df.apply(make_attendance_text, axis=1)
    return df

# ✅ 참석 정보 정리
def make_attendance_text(row):
    base = str(row.get('참석여부', '')).strip()
    detail = str(row.get('상세 참석여부', '')).strip()
    if base == '부분참' and detail and detail.lower() != 'nan':
        return f"{base} ({detail})"
    else:
        return base

df = load_data()

st.title("🧾 수련회 티셔츠 & 참석 정보 조회")

# ✅ 검색 로그 저장 함수
def log_search(name, found):
    log_folder = "logs"
    log_file = os.path.join(log_folder, "search_log.csv")
    os.makedirs(log_folder, exist_ok=True)

    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ip = st.session_state.get("remote_ip", "unknown")

    log_entry = pd.DataFrame([{
        "검색 시각": now,
        "검색어": name,
        "검색결과": "성공" if found else "실패",
        "IP": ip
    }])

    if os.path.exists(log_file):
        log_entry.to_csv(log_file, mode="a", header=False, index=False)
    else:
        log_entry.to_csv(log_file, index=False)

# ✅ 이름 검색 입력
name_query = st.text_input("🔍 이름을 입력하세요 (예: 이다솜(39))")

if name_query:
    result = df[df['이름'].str.contains(name_query, na=False)]
    log_search(name_query, not result.empty)

    if not result.empty:
        st.success(f"🔎 {len(result)}건의 결과가 검색되었습니다.")
        st.dataframe(result[['이름', '티셔츠 사이즈', '참석 정보']])
    else:
        st.warning("❌ 해당 이름을 찾을 수 없습니다.")
