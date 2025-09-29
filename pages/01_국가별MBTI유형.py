import pandas as pd
import plotly.express as px
import streamlit as st

# 페이지 설정
st.set_page_config(page_title="국가별 MBTI 프로필", layout="wide")

st.title("🌍 국가별 MBTI 프로필 대시보드")
st.caption("국가를 선택하면 해당 국가의 16개 MBTI 비율을 막대그래프로 보여줍니다. (값: 비율)")

# -----------------------
# 1) 데이터 로드
# -----------------------
@st.cache_data
def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    # 기본 검증: Country와 16개 MBTI 열 존재 여부
    assert "Country" in df.columns, "'Country' 열이 없습니다."
    return df

df = load_data("countriesMBTI_16types.csv")

# MBTI 열 목록
mbti_cols = [c for c in df.columns if c != "Country"]

# 국가 목록
countries = df["Country"].dropna().astype(str).tolist()

# -----------------------
# 2) 사이드바 - 국가 선택
# -----------------------
st.sidebar.header("⚙️ 설정")
default_country = "Korea, Republic of" if "Korea, Republic of" in countries else countries[0]
country = st.sidebar.selectbox("국가를 선택하세요", countries, index=countries.index(default_country))

# -----------------------
# 3) 선택 국가의 시리즈 → Long 형태 변환
# -----------------------
row = df.loc[df["Country"] == country, mbti_cols].iloc[0]
long_df = (
    row.reset_index(name="ratio")       # 안전하게 컬럼명 지정 (KeyError 방지 포인트)
       .rename(columns={"index": "MBTI"})
       .sort_values("ratio", ascending=False)
       .reset_index(drop=True)
)

# -----------------------
# 4) Plotly 막대 그래프
# -----------------------
# 보기 좋은 팔레트(Plotly 기본 + Set3 혼합)
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
fig.update_traces(
    hovertemplate="MBTI: %{x}<br>비율: %{y:.2%}<extra></extra>"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------
# 5) 상위 5개 표 하이라이트
# -----------------------
st.subheader("🏅 상위 5개 MBTI")
top5 = (
    long_df.head(5)
           .assign(**{"비율(%)": (long_df.head(5)["ratio"] * 100).round(2)})
           .drop(columns=["ratio"])
)
st.dataframe(top5, use_container_width=True)

st.caption("Tip: 사이드바에서 국가를 바꾸면 그래프와 표가 함께 갱신됩니다 ✨")
