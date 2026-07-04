import streamlit as st
import random
import time

# ----------------------------
# 페이지 설정
# ----------------------------
st.set_page_config(page_title="가위바위보 게임", page_icon="✊")

# ----------------------------
# 상태 초기화
# ----------------------------
if "page" not in st.session_state:
    st.session_state.page = "start"

if "score" not in st.session_state:
    st.session_state.score = {"player": 0, "computer": 0, "draw": 0}

if "result" not in st.session_state:
    st.session_state.result = None

if "player_choice" not in st.session_state:
    st.session_state.player_choice = None

if "computer_choice" not in st.session_state:
    st.session_state.computer_choice = None


# ----------------------------
# 스타일 (핑크-보라 그라데이션 + 카드 UI)
# ----------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #ff4ecd, #7b2ff7);
    color: white;
    font-family: 'Arial Rounded MT Bold', sans-serif;
}

/* 카드 */
.card {
    background: rgba(255,255,255,0.15);
    padding: 20px;
    border-radius: 20px;
    backdrop-filter: blur(10px);
    box-shadow: 0 8px 20px rgba(0,0,0,0.2);
    transition: 0.3s;
}

.card:hover {
    transform: translateY(-5px);
}

/* 버튼 */
.stButton > button {
    border-radius: 20px;
    padding: 12px 20px;
    font-size: 20px;
    font-weight: bold;
    background: white;
    color: #7b2ff7;
    border: none;
    transition: 0.3s;
}

.stButton > button:hover {
    transform: scale(1.08);
    background: #ffe6f7;
}

/* 결과 fade */
.fade {
    animation: fadeIn 0.8s ease-in;
}

@keyframes fadeIn {
    from {opacity: 0;}
    to {opacity: 1;}
}

/* 점수 애니메이션 */
.score-pop {
    display: inline-block;
    animation: pop 0.5s ease;
}

@keyframes pop {
    0% {transform: scale(0.7);}
    50% {transform: scale(1.3);}
    100% {transform: scale(1);}
}
</style>
""", unsafe_allow_html=True)


# ----------------------------
# 함수
# ----------------------------
def get_result(player, computer):
    if player == computer:
        return "무승부"
    elif (player == "바위" and computer == "가위") or \
         (player == "보" and computer == "바위") or \
         (player == "가위" and computer == "보"):
        return "승리"
    else:
        return "패배"


def update_score(result):
    if result == "승리":
        st.session_state.score["player"] += 1
    elif result == "패배":
        st.session_state.score["computer"] += 1
    else:
        st.session_state.score["draw"] += 1


# ----------------------------
# 시작 화면
# ----------------------------
if st.session_state.page == "start":

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown("## 🎮 가위 바위 보")

    if st.button("게임 시작"):
        st.session_state.page = "game"
        st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# ----------------------------
# 게임 화면
# ----------------------------
else:

    st.markdown("<div class='card fade'>", unsafe_allow_html=True)
    st.markdown("## ✊✌️✋ 가위 바위 보")

    # 점수판
    score = st.session_state.score
    st.markdown(f"""
    ### 🏆 점수판
    👤 플레이어 : {score['player']}  
    🤖 컴퓨터 : {score['computer']}  
    🤝 무승부 : {score['draw']}
    """)

    st.write("---")

    # 선택 안내
    st.markdown("### 선택해주세요!")

    col1, col2, col3 = st.columns(3)

    choices = ["가위", "바위", "보"]
    emojis = {"가위": "✌️", "바위": "✊", "보": "🖐️"}

    selected = None

    with col1:
        if st.button("✌️ 가위"):
            selected = "가위"
    with col2:
        if st.button("✊ 바위"):
            selected = "바위"
    with col3:
        if st.button("🖐️ 보"):
            selected = "보"

    # ----------------------------
    # 게임 진행 (0.5초 애니메이션 포함)
    # ----------------------------
    if selected:
        st.session_state.player_choice = selected

        with st.spinner("컴퓨터가 선택 중... 🤖"):
            time.sleep(0.5)

        st.session_state.computer_choice = random.choice(choices)

        result = get_result(selected, st.session_state.computer_choice)
        st.session_state.result = result

        update_score(result)

        st.rerun()


    # ----------------------------
    # 결과 출력
    # ----------------------------
    if st.session_state.result:

        st.write("---")

        st.markdown("### 🤖 컴퓨터 선택")
        st.markdown(f"## {emojis[st.session_state.computer_choice]} {st.session_state.computer_choice}")

        st.markdown("### 결과")
        st.markdown(f"## {st.session_state.result}")

        st.write("---")

        if st.button("🔄 다시하기 - 점수 초기화"):
            st.session_state.score = {"player": 0, "computer": 0, "draw": 0}
            st.session_state.result = None
            st.session_state.page = "start"
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)
