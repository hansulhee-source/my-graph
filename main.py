import streamlit as st
import pandas as pd
import plotly.express as px

# 1. 페이지 설정 및 제목
st.set_page_config(page_title="영화 데이터 그래프 도감 1 - 시간", layout="wide")
st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.markdown("1년치(365일) 일별 박스오피스 데이터를 바탕으로 시간의 흐름에 따른 변화를 시각화합니다.")
st.write("---")

# 2. 데이터 로드 및 전처리
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    # 날짜 열을 YYYYMMDD 형태에서 datetime 객체로 변환
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    return df

df = load_data()

# 3. 구역 1: 영화별 일일 관객수 변화 (선 그래프)
st.header("📌 구역 1. 영화별 일일 관객수 추이")

# 영화 선택 드롭다운 (관객수 총합 기준 내림차순 정렬)
movie_list = df.groupby("영화명")["일관객"].sum().sort_values(ascending=False).index.tolist()
selected_movie = st.selectbox("영화를 선택하세요:", movie_list)

# 선택된 영화 데이터 필터링
movie_df = df[df["영화명"] == selected_movie].sort_values("날짜")

# Plotly 선 그래프 생성
fig1 = px.line(
    movie_df, 
    x="날짜", 
    y="일관객", 
    title=f"[{selected_movie}] 일별 관객수 변화",
    labels={"날짜": "날짜", "일관객": "일일 관객수(명)"},
    markers=True,
    hover_data={"날짜": "|%Y-%m-%d", "일관객": ":,d"}
)

fig1.update_traces(
    hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객:</b> %{y:,}명<extra></extra>"
)

fig1.update_layout(
    xaxis_title="날짜",
    yaxis_title="일일 관객수(명)",
    hovermode="x unified"
)

st.plotly_chart(fig1, use_container_width=True)

# 그래프 해석/시사점 작성 공간
st.info(f"💡 **이 그래프로 알 수 있는 것:** 개봉 후 시간 경과에 따른 [{selected_movie}]의 흥행 추이 및 주말/평일 간 관객수 변동 패턴을 파악할 수 있습니다.")

st.write("---")

# 4. 향후 그래프 추가를 위한 예시 구역 (확장 구역)
st.header("📌 구역 2. [추가 예정] 시간 기반 비교 시각화")
st.write("👉 *다음 그래프가 여기에 추가될 예정입니다 (예: 누적 관객수 추이, 요일별 관객수 분포 등).*")
