import random
import pandas as pd
import streamlit as st

# 페이지 기본 설정
st.set_page_config(
    page_title="가위바위보 챌린지",
    page_icon="🎮",
    layout="centered",
)

# 커스텀 스타일 (고등학생이 보기 좋게 깔끔하고 직관적인 카드/이모지 크기 조정)
st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(ellipse at 12% 12%, rgba(255, 190, 92, 0.38) 0%, transparent 32%),
            radial-gradient(ellipse at 88% 18%, rgba(255, 117, 168, 0.30) 0%, transparent 34%),
            radial-gradient(ellipse at 78% 82%, rgba(85, 186, 255, 0.30) 0%, transparent 36%),
            linear-gradient(135deg, #fff8e7 0%, #f8edff 48%, #e8f7ff 100%);
        background-attachment: fixed;
    }
    .big-emoji {
        font-size: 4.5rem;
        text-align: center;
        line-height: 1.2;
        margin: 10px 0;
    }
    .choice-label {
        font-size: 1.2rem;
        font-weight: 700;
        text-align: center;
    }
    .vs-text {
        font-size: 2rem;
        font-weight: 900;
        text-align: center;
        color: #FF4B4B;
        padding-top: 38px;
    }
    div.stButton > button {
        width: 100%;
        height: 3.5rem;
        font-size: 1.2rem;
        font-weight: 700;
        border-radius: 12px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 전적 및 상태 저장을 위한 세션 상태 초기화
if "wins" not in st.session_state:
    st.session_state.wins = 0
if "losses" not in st.session_state:
    st.session_state.losses = 0
if "draws" not in st.session_state:
    st.session_state.draws = 0
if "streak" not in st.session_state:
    st.session_state.streak = 0
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "history" not in st.session_state:
    st.session_state.history = []

# 선택지 데이터 정의
CHOICES = {
    "가위": "✌️",
    "바위": "✊",
    "보": "🖐️",
}


def get_winner(user_choice: str, computer_choice: str) -> str:
    """승패를 판정하는 함수"""
    if user_choice == computer_choice:
        return "무승부"
    elif (
        (user_choice == "가위" and computer_choice == "보")
        or (user_choice == "바위" and computer_choice == "가위")
        or (user_choice == "보" and computer_choice == "바위")
    ):
        return "승리"
    else:
        return "패배"


def play_round(user_choice: str):
    """사용자가 버튼을 눌렀을 때 한 라운드를 진행하는 함수"""
    computer_choice = random.choice(list(CHOICES.keys()))
    result = get_winner(user_choice, computer_choice)

    # 전적 및 연승 업데이트
    if result == "승리":
        st.session_state.wins += 1
        st.session_state.streak += 1
    elif result == "패배":
        st.session_state.losses += 1
        st.session_state.streak = 0
    else:
        st.session_state.draws += 1

    # 현재까지의 누적 라운드 및 승률 계산
    round_num = st.session_state.wins + st.session_state.losses + st.session_state.draws
    current_win_rate = round((st.session_state.wins / round_num) * 100, 1)

    # 라운드별 기록 저장 (그래프 및 표 생성용)
    st.session_state.history.append(
        {
            "라운드": round_num,
            "나": f"{CHOICES[user_choice]} {user_choice}",
            "컴퓨터": f"{CHOICES[computer_choice]} {computer_choice}",
            "결과": result,
            "누적 승리": st.session_state.wins,
            "누적 패배": st.session_state.losses,
            "누적 무승부": st.session_state.draws,
            "승률(%)": current_win_rate,
        }
    )

    # 최근 경기 결과 저장
    st.session_state.last_result = {
        "user": user_choice,
        "computer": computer_choice,
        "result": result,
    }


def reset_game():
    """점수판 및 그래프 기록 초기화 함수"""
    st.session_state.wins = 0
    st.session_state.losses = 0
    st.session_state.draws = 0
    st.session_state.streak = 0
    st.session_state.last_result = None
    st.session_state.history = []


# 1) 화면 상단 제목
st.title("🎮 가위바위보 챌린지")
st.caption("컴퓨터와의 심리전! 연승 기록과 실시간 승률 그래프에 도전해 보세요 🔥")

# 실시간 스코어보드
total_games = st.session_state.wins + st.session_state.losses + st.session_state.draws
win_rate = (st.session_state.wins / total_games * 100) if total_games > 0 else 0.0

score_col1, score_col2, score_col3, score_col4 = st.columns(4)
score_col1.metric("🏆 승리", f"{st.session_state.wins}회")
score_col2.metric("😭 패배", f"{st.session_state.losses}회")
score_col3.metric("🤝 무승부", f"{st.session_state.draws}회")
score_col4.metric("🔥 연승 / 승률", f"{st.session_state.streak}연승 ({win_rate:.0f}%)")

st.divider()

# 2) 사용자 선택 영역
st.subheader("👇 무엇을 낼까요? 하나를 선택하세요!")
btn_col1, btn_col2, btn_col3 = st.columns(3)

with btn_col1:
    st.button("✌️ 가위", on_click=play_round, args=("가위",), use_container_width=True)
with btn_col2:
    st.button("✊ 바위", on_click=play_round, args=("바위",), use_container_width=True)
with btn_col3:
    st.button("🖐️ 보", on_click=play_round, args=("보",), use_container_width=True)

st.divider()

# 3) 선택 결과 및 승패 출력 영역
if st.session_state.last_result is not None:
    user_pick = st.session_state.last_result["user"]
    comp_pick = st.session_state.last_result["computer"]
    outcome = st.session_state.last_result["result"]

    res_col1, res_col2, res_col3 = st.columns([2, 1, 2])

    with res_col1:
        st.markdown('<div class="choice-label">🙋‍♂️ 나 (Player)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="big-emoji">{CHOICES[user_pick]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="choice-label">{user_pick}</div>', unsafe_allow_html=True)

    with res_col2:
        st.markdown('<div class="vs-text">VS</div>', unsafe_allow_html=True)

    with res_col3:
        st.markdown('<div class="choice-label">🤖 컴퓨터 (AI)</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="big-emoji">{CHOICES[comp_pick]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="choice-label">{comp_pick}</div>', unsafe_allow_html=True)

    st.write("")

    # 결과 메시지 표시
    if outcome == "승리":
        if st.session_state.streak >= 3:
            st.success(f"🎉 대박! {st.session_state.streak}연승 달성! 당신이 이겼습니다! 🏆")
            st.balloons()
        else:
            st.success("🎉 승리! 컴퓨터를 이겼습니다! 😎")
    elif outcome == "패배":
        st.error("💥 패배! 컴퓨터가 이겼네요. 다음 판에 복수해 봅시다! 💪")
    else:
        st.info("🤝 무승부! 둘 다 같은 것을 냈어요. 한 번 더 승부해 보세요!")
else:
    st.info("👆 위에서 **가위, 바위, 보** 중 하나를 클릭하면 대결이 시작됩니다!")

# 4) 가위바위보 결과 그래프 및 라운드 기록 영역
if total_games > 0:
    st.divider()
    st.subheader("📊 대결 결과 그래프")

    history_df = pd.DataFrame(st.session_state.history)

    tab1, tab2, tab3 = st.tabs(["📊 승패 횟수 비교", "📈 라운드별 승률 변화", "📝 상세 기록표"])

    with tab1:
        summary_df = pd.DataFrame(
            {
                "결과": ["🏆 승리", "😭 패배", "🤝 무승부"],
                "횟수": [
                    st.session_state.wins,
                    st.session_state.losses,
                    st.session_state.draws,
                ],
            }
        ).set_index("결과")
        st.bar_chart(summary_df, color="#FF4B4B")

    with tab2:
        rate_df = history_df[["라운드", "승률(%)"]].set_index("라운드")
        st.line_chart(rate_df, color="#29B5E8")
        st.caption("라운드가 진행될수록 내 승률(%)이 어떻게 변하는지 확인할 수 있어요.")

    with tab3:
        display_df = history_df[["라운드", "나", "컴퓨터", "결과", "승률(%)"]].sort_values(
            by="라운드", ascending=False
        )
        st.dataframe(display_df, use_container_width=True, hide_index=True)

    # 하단 초기화 버튼
    st.write("")
    st.button("🔄 기록 및 그래프 초기화", on_click=reset_game)
