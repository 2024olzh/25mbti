import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="국가별 MBTI 프로필", layout="wide")
st.title("🌍 국가를 선택하면 보이는 MBTI 프로필")
st.caption("한 나라의 16개 MBTI 분포를 막대그래프로 비교해요. (값은 비율)")

# 1) 데이터 로드
df = pd.read_csv("countriesMBTI_16types.csv")

# 2) 컬럼 구분
mbti_cols = [c for c in df.columns if c != "Country"]
countries = df["Country"].tolist()

# 3) 사이드바 - 국가 선택
st.sidebar.header("⚙️ 설정")
default_country = "Korea, Republic of" if "Korea, Republic of" in countries else countries[0]
country = st.sidebar.selectbox("국가를 선택하세요", countries, index=countries.index(default_country))

# 4) 선택 국가의 데이터 추출 및 Long 형태로 변환
row = df[df["Country"] == country][mbti_cols].iloc[0]
long_df = (
    row.reset_index()
       .rename(columns={"index": "MBTI", 0: "ratio"})
       .sort_values("ratio", ascending=False)
)

# 5) 색상 팔레트(센스있게 쾌적한 톤) & 차트
#   - MBTI 16유형 각각 다른 색상
palette = px.colors.qualitative.Plotly + px.colors.qualitative.Set3

fig = px.bar(
    long_df,
    x="MBTI",
    y="ratio",
    color="MBTI",
    color_discrete_sequence=palette,
    text=long_df["ratio"].map(lambda v: f"{v:.1%}"),
    labels={"MBTI": "MBTI 유형", "ratio": "비율"},
    title=f"🇺🇳 {country} 의 MBTI 분포 📊",
)
fig.update_layout(
    template="plotly_white",
    showlegend=False,
    margin=dict(l=20, r=20, t=60, b=20),
    yaxis_tickformat=".0%",
)
fig.update_traces(hovertemplate="MBTI: %{x}<br>비율: %{y:.2%}<extra></extra>")

# 6) 표시
st.plotly_chart(fig, use_container_width=True)

# 7) 상위 5개 하이라이트 표
st.subheader("🏅 상위 5개 MBTI")
st.dataframe(
    long_df.head(5).reset_index(drop=True).assign(ratio=lambda d: (d["ratio"]*100).round(2)).rename(columns={"ratio": "비율(%)"}),
    use_container_width=True
)

st.caption("Tip: 사이드바에서 국가를 바꿔보세요. 그래프와 표가 함께 갱신됩니다 ✨")
