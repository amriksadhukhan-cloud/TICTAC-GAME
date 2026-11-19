import streamlit as st
import random

# ---------------- PAGE CONFIGURATION ----------------

st.set_page_config(
    page_title="Tic Tac Toe Game",
    page_icon="🎮",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #101827, #202f46);
    color: white;
}

h1 {
    text-align: center;
    color: #ffffff;
    font-weight: 800;
}

.subtitle {
    text-align: center;
    color: #aab8cc;
    font-size: 16px;
}

div.stButton > button {
    height: 95px;
    width: 100%;
    font-size: 38px;
    font-weight: bold;
    border-radius: 15px;
    background: #263750;
    color: white;
    border: 2px solid #435875;
    transition: 0.2s;
}

div.stButton > button:hover {
    background: #3b5272;
    border-color: #38bdf8;
    color: white;
}

div.stButton > button:disabled {
    background: #263750;
    color: white;
    border-color: #435875;
    opacity: 1;
}

div[data-testid="stMetric"] {
    background: #263750;
    padding: 15px;
    border-radius: 12px;
    border: 1px solid #435875;
}

</style>
""", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------

if "board" not in st.session_state:
    st.session_state.board = [""] * 9

if "current_player" not in st.session_state:
    st.session_state.current_player = "X"

if "winner" not in st.session_state:
    st.session_state.winner = None

if "draw" not in st.session_state:
    st.session_state.draw = False

if "scores" not in st.session_state:
    st.session_state.scores = {"X": 0, "O": 0, "Draw": 0}

if "mode" not in st.session_state:
    st.session_state.mode = "Two Player"

# ---------------- WINNING COMBINATIONS ----------------

winning_combinations = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

# ---------------- CHECK WINNER ----------------

def check_winner(board):

    for combination in winning_combinations:

        a, b, c = combination

        if (
            board[a] != ""
            and board[a] == board[b] == board[c]
        ):
            return board[a]

    return None


# ---------------- GAME OVER CHECK ----------------

def game_over():

    return (
        st.session_state.winner is not None
        or st.session_state.draw
    )


# ---------------- REGISTER RESULT ----------------

def register_result():

    winner = check_winner(st.session_state.board)

    if winner:

        st.session_state.winner = winner
        st.session_state.scores[winner] += 1

    elif "" not in st.session_state.board:

        st.session_state.draw = True
        st.session_state.scores["Draw"] += 1


# ---------------- COMPUTER AI ----------------

def find_best_move(player):

    board = st.session_state.board

    # Check winning or blocking opportunities

    for position in range(9):

        if board[position] == "":

            board[position] = player

            if check_winner(board):
                board[position] = ""
                return position

            board[position] = ""

    return None


def computer_move():

    board = st.session_state.board

    # 1. Try to win

    position = find_best_move("O")

    # 2. Block player X from winning

    if position is None:
        position = find_best_move("X")

    # 3. Take center if available

    if position is None and board[4] == "":
        position = 4

    # 4. Take a corner

    if position is None:

        corners = [0, 2, 6, 8]

        available_corners = [
            i for i in corners if board[i] == ""
        ]

        if available_corners:
            position = random.choice(available_corners)

    # 5. Select any available position

    if position is None:

        available = [
            i for i in range(9) if board[i] == ""
        ]

        if available:
            position = random.choice(available)

    if position is not None:

        board[position] = "O"

        register_result()

        if not game_over():
            st.session_state.current_player = "X"


# ---------------- PLAYER MOVE ----------------

def make_move(position):

    if game_over():
        return

    if st.session_state.board[position] != "":
        return

    st.session_state.board[position] = (
        st.session_state.current_player
    )

    register_result()

    if game_over():
        return

    if st.session_state.mode == "Computer":

        st.session_state.current_player = "O"
        computer_move()

    else:

        st.session_state.current_player = (
            "O" if st.session_state.current_player == "X" else "X"
        )


# ---------------- RESET GAME ----------------

def reset_game():

    st.session_state.board = [""] * 9
    st.session_state.current_player = "X"
    st.session_state.winner = None
    st.session_state.draw = False


def reset_scores():

    reset_game()

    st.session_state.scores = {
        "X": 0,
        "O": 0,
        "Draw": 0
    }


# ---------------- HEADER ----------------

st.markdown(
    "<h1>🎮 TIC TAC TOE</h1>",
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Challenge your friend or defeat the AI computer!</p>',
    unsafe_allow_html=True
)

st.divider()

# ---------------- GAME MODE ----------------

mode = st.selectbox(
    "🎯 Select Game Mode",
    ["Two Player", "Computer"],
    index=0 if st.session_state.mode == "Two Player" else 1
)

if mode != st.session_state.mode:

    st.session_state.mode = mode
    reset_game()
    st.rerun()

# ---------------- SCOREBOARD ----------------

st.subheader("🏆 Scoreboard")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("❌ Player X", st.session_state.scores["X"])

with col2:
    opponent_name = (
        "🤖 Computer" if mode == "Computer" else "⭕ Player O"
    )
    st.metric(opponent_name, st.session_state.scores["O"])

with col3:
    st.metric("🤝 Draws", st.session_state.scores["Draw"])

st.divider()

# ---------------- GAME STATUS ----------------

if st.session_state.winner:

    if mode == "Computer" and st.session_state.winner == "O":
        st.error("🤖 Computer Wins! Better luck next time!")

    else:
        st.success(
            f"🏆 Player {st.session_state.winner} Wins!"
        )

elif st.session_state.draw:

    st.warning("🤝 It's a Draw! Great Match!")

else:

    if mode == "Computer" and st.session_state.current_player == "X":
        st.info("🎯 Your Turn! You are ❌")

    elif mode == "Computer":
        st.info("🤖 Computer's Turn")

    else:
        st.info(
            f"🎯 Player {st.session_state.current_player}'s Turn"
        )

# ---------------- GAME BOARD ----------------

for row in range(3):

    cols = st.columns(3)

    for col in range(3):

        position = row * 3 + col

        with cols[col]:

            symbol = st.session_state.board[position]

            if symbol == "X":
                label = "❌"

            elif symbol == "O":
                label = "⭕"

            else:
                label = " "

            st.button(
                label,
                key=f"cell_{position}",
                on_click=make_move,
                args=(position,),
                disabled=(
                    symbol != ""
                    or game_over()
                    or (
                        mode == "Computer"
                        and st.session_state.current_player == "O"
                    )
                ),
                use_container_width=True
            )

# ---------------- RESULT MESSAGE ----------------

if st.session_state.winner:

    st.markdown(
        f"""
        <div style="
            text-align:center;
            background:#164e3b;
            padding:18px;
            border-radius:12px;
            font-size:22px;
            font-weight:bold;
            margin-top:15px;
        ">
        🎉 Player {st.session_state.winner} is the Champion!
        </div>
        """,
        unsafe_allow_html=True
    )

elif st.session_state.draw:

    st.markdown(
        """
        <div style="
            text-align:center;
            background:#57451c;
            padding:18px;
            border-radius:12px;
            font-size:22px;
            font-weight:bold;
            margin-top:15px;
        ">
        🤝 Match Draw!
        </div>
        """,
        unsafe_allow_html=True
    )

# ---------------- GAME CONTROLS ----------------

st.divider()

col1, col2 = st.columns(2)

with col1:

    st.button(
        "🔄 New Game",
        on_click=reset_game,
        use_container_width=True
    )

with col2:

    st.button(
        "🗑️ Reset Scores",
        on_click=reset_scores,
        use_container_width=True
    )

# ---------------- FOOTER ----------------

st.markdown("""
<p style="
    text-align:center;
    color:#8495aa;
    margin-top:25px;
">
Made with ❤️ using Python and Streamlit
</p>
""", unsafe_allow_html=True)
