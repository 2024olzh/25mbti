import pandas as pd
import altair as alt
import streamlit as st

st.set_page_config(page_title="MBTI 상위 10개국 차트", layout="wide")
st.title("🌍 MBTI 유형별 상위 10개국 막대 그래프")

# 1) 데이터 로드
df = pd.read_csv("countriesMBTI_16types.csv")

# 2) MBTI 컬럼 목록
mbti_cols = [c for c in df.columns if c != "Country"]

# 3) 사이드바에서 MBTI 유형 선택
st.sidebar.header("설정")
selected = st.sidebar.selectbox("MBTI 유형을 선택하세요", mbti_cols, index=mbti_cols.index("INFP") if "INFP" in mbti_cols else 0)

# 4) 선택된 유형의 상위 10개국 추출
top_n = 10
top_df = (
    df[["Country", selected]]
    .nlargest(top_n, selected)
    .sort_values(selected, ascending=True)  # 가독성을 위해 작은 값→큰 값
    .rename(columns={selected: "ratio"})
)

st.subheader(f"✅ {selected} 비율 상위 {top_n}개국")
st.dataframe(top_df.rename(columns={"ratio": f"{selected}"}), use_container_width=True)

# 5) Altair 막대 그래프
chart = (
    alt.Chart(top_df)
    .mark_bar()
    .encode(
        x=alt.X("ratio:Q", title=f"{selected} 비율", axis=alt.Axis(format=".1%")),
        y=alt.Y("Country:N", sort="-x", title="국가"),
        tooltip=[
            alt.Tooltip("Country:N", title="국가"),
            alt.Tooltip("ratio:Q", title="비율", format=".2%")
        ],
    )
    .properties(height=420)
)

st.altair_chart(chart, use_container_width=True)

# 6) 간단한 설명
st.caption("Tip: 사이드바에서 MBTI 유형을 바꾸면 해당 유형의 상위 10개국이 갱신됩니다.")
