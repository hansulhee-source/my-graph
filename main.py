
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
    markers=True
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

# 4. 구역 2: 상위 5개 영화 일일 관객수 비교 (선 그래프)
st.header("📌 구역 2. 기간 내 관객수 상위 5개 영화 비교")

# 일관객 합계 기준 상위 5개 영화 추출
top5_movies = df.groupby("영화명")["일관객"].sum().nlargest(5).index.tolist()

# 상위 5개 영화 데이터 필터링
top5_df = df[df["영화명"].isin(top5_movies)].sort_values("날짜")

# Plotly 다중 선 그래프 생성 (색상으로 영화 구분)
fig2 = px.line(
    top5_df,
    x="날짜",
    y="일관객",
    color="영화명",
    title="기간 내 일관객 합계 상위 5개 영화의 일별 관객수 비교",
    labels={"날짜": "날짜", "일관객": "일일 관객수(명)", "영화명": "영화 제목"}
)

fig2.update_traces(
    hovertemplate="<b>영화명:</b> %{fullData.name}<br><b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객:</b> %{y:,}명<extra></extra>"
)

fig2.update_layout(
    xaxis_title="날짜",
    yaxis_title="일일 관객수(명)",
    hovermode="x unified",
    legend_title_text="영화 목록 (클릭하여 켜기/끄기)"
)

st.plotly_chart(fig2, use_container_width=True)

# 그래프 해석/시사점 작성 공간
top5_names_str = ", ".join(top5_movies)
st.info(f"💡 **이 그래프로 알 수 있는 것:** 기간 내 가장 많은 관객을 동원한 상위 5개 영화({top5_names_str})의 개봉 시기별 흥행 화력과 최고 전성기 스파이크를 상호 비교할 수 있습니다.")

st.write("---")

# 5. 구역 3: 날짜별 10위권 일관객 총합 추이 (영역 그래프)
st.header("📌 구역 3. 날짜별 박스오피스 TOP 10 전체 관객수 총합")

# 날짜별 10위권 일관객 총합 계산
daily_total = df.groupby("날짜")["일관객"].sum().reset_index()

# 관객수 총합 기준 상위 3개 날짜 추출
top3_days = daily_total.nlargest(3, "일관객").sort_values("날짜")

# Plotly 영역 그래프 생성
fig3 = px.area(
    daily_total,
    x="날짜",
    y="일관객",
    title="일별 박스오피스 TOP 10 관객수 총합 변화 (영역 그래프)",
    labels={"날짜": "날짜", "일관객": "10위권 총 관객수(명)"}
)

fig3.update_traces(
    hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>TOP 10 총 관객수:</b> %{y:,}명<extra></extra>"
)

# 상위 3일 주석(Annotation) 표시 및 마커 추가
for idx, row in top3_days.iterrows():
    date_str = row["날짜"].strftime("%Y-%m-%d")
    val = row["일관객"]
    
    # 해당 포인트에 붉은색 마커 표기
    fig3.add_scatter(
        x=[row["날짜"]],
        y=[val],
        mode="markers",
        marker=dict(size=10, color="red"),
        showlegend=False,
        hoverinfo="skip"
    )
    
    # 텍스트 주석 추가
    fig3.add_annotation(
        x=row["날짜"],
        y=val,
        text=f"<b>{date_str}</b><br>({val:,}명)",
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=1.5,
        arrowcolor="red",
        ax=0,
        ay=-45,
        font=dict(size=11, color="red")
    )

fig3.update_layout(
    xaxis_title="날짜",
    yaxis_title="TOP 10 총 관객수(명)",
    hovermode="x unified"
)

st.plotly_chart(fig3, use_container_width=True)

# 그래프 해석/시사점 작성 공간
top3_dates_str = ", ".join([d.strftime('%Y년 %m월 %d일') for d in top3_days["날짜"]])
st.info(f"💡 **이 그래프로 알 수 있는 것:** 연중 영화 시장 전체가 가장 활황이었던 최고 피크일 Top 3({top3_dates_str})를 한눈에 확인하고, 연휴나 성수기 시즌의 극장가 관객 집중도를 파악할 수 있습니다.")

st.write("---")

# 6. 향후 그래프 추가를 위한 확장 구역
st.header("📌 구역 4. [추가 예정] 시간 기반 분석 시각화")
st.write("👉 *다음 그래프가 여기에 추가될 예정입니다.*")
