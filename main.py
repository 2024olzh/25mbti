import pandas as pd
import streamlit as st

# 제목
st.title("MBTI 국가별 데이터 미리보기")

# CSV 파일 불러오기 (같은 폴더에 있다고 가정)
df = pd.read_csv("countriesMBTI_16types.csv")

# 상위 5줄만 표시
st.subheader("데이터 상위 5줄")
st.dataframe(df.head())

