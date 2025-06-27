import streamlit as st
import pandas as pd

# 비밀번호 설정
PASSWORD = "1234"  # 원하는 비밀번호로 바꿔주세요

# 엑셀 파일 경로
EXCEL_FILE = "data/tshirt_info_2025.xlsx"

# 데이터 불러오기 @st.cache_data로 캐싱
def load_data():
    df = pd.read_excel(EXCEL_FILE)
    return df

# 앱 제목
st.title("수련회 티셔츠 & 참석 정보 조회")

# 비밀번호 입력
password_input = st.text_input("\U0001F511 비밀번호 4자리를 입력하세요", type="password")

if password_input == PASSWORD:
    df = load_data()

    # 이름 입력
    name_input = st.text_input("\U0001F464 이름을 입력하세요 (예: 이다솜)")

    if name_input:
        try:
            # '이름' 열만 남기고 숫자 열 제거 (이름 포함된 셀만 필터링)
            if "이름" not in df.columns:
                st.error("엑셀 파일에 '이름'이라는 열이 존재하지 않습니다.")
            else:
                # 이름 포함된 행 추출 (띄어쓰기 제거하고 비교)
                filtered_df = df[df["이름"].astype(str).str.contains(name_input.strip())]

                if filtered_df.empty:
                    st.warning(f"'{name_input}'에 해당하는 정보를 찾을 수 없습니다.")
                else:
                    st.success(f"'{name_input}'에 대한 조회 결과입니다.")
                    st.dataframe(filtered_df)
        except Exception as e:
            st.error(f"에러가 발생했습니다: {e}")
else:
    if password_input != "":
        st.error("비밀번호가 틀렸습니다.")
