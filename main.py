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
    
    fig3.add_scatter(
        x=[row["날짜"]],
        y=[val],
        mode="markers",
        marker=dict(size=10, color="red"),
        showlegend=False,
        hoverinfo="skip"
    )
    
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

# 6. 구역 4: 기간 내 누적 관객수 TOP 10 영화 (가로 막대그래프)
st.header("📌 구역 4. 기간 내 누적 관객수 TOP 10 영화")

# 영화별 일관객 합계 및 10위권 차트인 날수(진입 일수) 집계
movie_summary = df.groupby("영화명").agg(
    총관객수=("일관객", "sum"),
    차트인일수=("날짜", "nunique")
).reset_index()

# 총관객수 기준 상위 10개 영화 추출
top10_movies_df = movie_summary.nlargest(10, "총관객수").sort_values("총관객수", ascending=True)

# Plotly 가로 막대그래프 생성
fig4 = px.bar(
    top10_movies_df,
    x="총관객수",
    y="영화명",
    orientation="h",
    title="기간 내 일관객 합계 TOP 10 영화",
    labels={"총관객수": "누적 관객수(명)", "영화명": "영화 제목"},
    text_auto=",.0f",
    color="총관객수",
    color_continuous_scale="Viridis"
)

# 마우스 오버(Hover) 시 10위권 진입 날수 표시
fig4.update_traces(
    customdata=top10_movies_df[["차트인일수"]],
    hovertemplate="<b>영화명:</b> %{y}<br><b>누적 관객수:</b> %{x:,}명<br><b>TOP 10 진입 일수:</b> %{customdata[0]}일<extra></extra>"
)

fig4.update_layout(
    xaxis_title="누적 관객수(명)",
    yaxis_title="영화 제목",
    coloraxis_showscale=False
)

st.plotly_chart(fig4, use_container_width=True)

# 그래프 해석/시사점 작성 공간
top_1_movie = top10_movies_df.iloc[-1]["영화명"]
top_1_days = top10_movies_df.iloc[-1]["차트인일수"]
st.info(f"💡 **이 그래프로 알 수 있는 것:** 기간 중 가장 많은 전체 관객을 동원한 최상위 흥행작 10편의 세부 실적과, 1위 영화인 [{top_1_movie}] 등이 TOP 10 차트에 며칠 동안 유효하게 머물렀는지(롱런 여부({top_1_days}일))를 쉽게 비교할 수 있습니다.")

st.write("---")

# 7. 구역 5: 월×요일별 일관객 합계 히트맵
st.header("📌 구역 5. 월 × 요일별 일관객 합계 히트맵")

# 데이터 복사 및 월, 요일 추출
df_heatmap = df.copy()
df_heatmap['월'] = df_heatmap['날짜'].dt.strftime('%m월')
df_heatmap['요일'] = df_heatmap['날짜'].dt.day_name()

# 요일 한글 변환 및 정렬 순서 정의 (월요일 -> 일요일)
day_map = {
    'Monday': '월요일',
    'Tuesday': '화요일',
    'Wednesday': '수요일',
    'Thursday': '목요일',
    'Friday': '금요일',
    'Saturday': '토요일',
    'Sunday': '일요일'
}
day_order = ['월요일', '화요일', '수요일', '목요일', '금요일', '토요일', '일요일']

df_heatmap['요일'] = df_heatmap['요일'].map(day_map)

# 피벗 테이블 생성 (월 x 요일별 일관객 합계)
heatmap_pivot = df_heatmap.pivot_table(
    index='월',
    columns='요일',
    values='일관객',
    aggfunc='sum'
).reindex(columns=day_order).fillna(0)

# Plotly 히트맵 생성 (관객이 많을수록 색이 진해지도록 Viridis 컬러팔레트 사용)
fig5 = px.imshow(
    heatmap_pivot,
    labels=dict(x="요일", y="월", color="총 관객수(명)"),
    x=day_order,
    y=heatmap_pivot.index,
    title="월 및 요일별 일관객 합계 히트맵",
    color_continuous_scale="Viridis",
    aspect="auto"
)

fig5.update_traces(
    hovertemplate="<b>월:</b> %{y}<br><b>요일:</b> %{x}<br><b>관객수 합계:</b> %{z:,}명<extra></extra>"
)

fig5.update_layout(
    xaxis_title="요일",
    yaxis_title="월"
)

st.plotly_chart(fig5, use_container_width=True)

# 히트맵 상 최다 관객 월/요일 조합 추출
max_val = heatmap_pivot.values.max()
max_pos = heatmap_pivot.stack().idxmax() # (월, 요일)

st.info(f"💡 **이 그래프로 알 수 있는 것:** 월별/요일별 극장 관객 집중 패턴을 파악할 수 있으며, 이 데이터 세트에서는 **{max_pos[0]} {max_pos[1]}**에 가장 높은 관객수({int(max_val):,}명)를 기록하여 최고의 성수기 요일 및 시즌임을 알 수 있습니다.")

st.write("---")

# 8. 향후 그래프 추가를 위한 확장 구역
st.header("📌 구역 6. [추가 예정] 시간 기반 분석 시각화")
st.write("👉 *다음 그래프가 여기에 추가될 예정입니다.*")
