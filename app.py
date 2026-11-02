import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="가위바위보 챌린지", page_icon="🎮", layout="centered")

# 1) 화면 상단 제목
st.title("🎮 가위바위보 챌린지 🎮")
st.markdown("컴퓨터와 가위바위보 대결을 펼쳐보세요! 운을 시험해 볼 시간입니다. 😎")

# 이모지 매핑
choices = {"가위": "✂️", "바위": "✊", "보": "🖐️"}
options = list(choices.keys())

st.divider()

# 2) 사용자 선택
st.subheader("당신의 선택은?")
user_choice = st.radio("아래에서 하나를 고르세요:", options, horizontal=True)

if st.button("결과 확인하기 🚀"):
    st.divider()
    
    # 3) 컴퓨터 랜덤 선택
    computer_choice = random.choice(options)

    # 4) 사용자와 컴퓨터의 선택 화면 출력
    col1, col2 = st.columns(2)
    with col1:
        st.info("🧑‍🎓 당신의 선택")
        st.markdown(f"<h1 style='text-align: center;'>{choices[user_choice]}<br>{user_choice}</h1>", unsafe_allow_html=True)
    
    with col2:
        st.info("💻 컴퓨터의 선택")
        st.markdown(f"<h1 style='text-align: center;'>{choices[computer_choice]}<br>{computer_choice}</h1>", unsafe_allow_html=True)

    # 5) 승리, 패배, 무승부 결과 판별 및 6) 이모지 활용
    st.markdown("<br>", unsafe_allow_html=True)
    if user_choice == computer_choice:
        st.warning("## 무승부! 😅 다시 도전해보세요.")
    elif (user_choice == "가위" and computer_choice == "보") or \
         (user_choice == "바위" and computer_choice == "가위") or \
         (user_choice == "보" and computer_choice == "바위"):
        st.success("## 당신의 승리! 🎉 축하합니다!")
        st.balloons() # 7) 깔끔하고 재미있는 효과
    else:
        st.error("## 컴퓨터의 승리! 😭 아쉽네요.")
