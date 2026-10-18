
import streamlit as st
from collections import deque

st.set_page_config(page_title="AI Maze Runner", page_icon="🎮")

st.title("🎮 AI Maze Runner")
st.write("Can you reach the goal before the AI?")

maze = [
    ['S', '#', '.', '.', '.', '.', '.', '.'],
    ['.', '#', '.', '#', '#', '#', '.', '.'],
    ['.', '.', '.', '.', '.', '#', '.', '.'],
    ['#', '#', '#', '#', '.', '#', '.', '.'],
    ['.', '.', '.', '.', '.', '.', '.', '.'],
    ['.', '#', '#', '#', '#', '#', '#', '.'],
    ['.', '.', '.', '.', '.', '.', '#', '.'],
    ['.', '#', '#', '#', '#', '.', '.', 'G']
]

START = (0, 0)
GOAL = (7, 7)
ROWS, COLS = len(maze), len(maze[0])

def find_path():
    queue = deque([(START, [START])])
    visited = {START}

    while queue:
        (r, c), path = queue.popleft()

        if (r, c) == GOAL:
            return path

        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc

            if (
                0 <= nr < ROWS
                and 0 <= nc < COLS
                and maze[nr][nc] != '#'
                and (nr, nc) not in visited
            ):
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))

    return []

path = find_path()

if not path:
    st.error("No path to the goal!")
    st.stop()

if "player" not in st.session_state:
    st.session_state.player = START
    st.session_state.ai_step = 0
    st.session_state.finished = False
    st.session_state.message = ""

def reset_game():
    st.session_state.player = START
    st.session_state.ai_step = 0
    st.session_state.finished = False
    st.session_state.message = ""

def move_player(dr, dc):
    if st.session_state.finished:
        return

    r, c = st.session_state.player
    nr, nc = r + dr, c + dc

    if (
        0 <= nr < ROWS
        and 0 <= nc < COLS
        and maze[nr][nc] != '#'
    ):
        st.session_state.player = (nr, nc)

    if st.session_state.player == GOAL:
        st.session_state.finished = True
        st.session_state.message = "🏆 You win!"

    if not st.session_state.finished:
        st.session_state.ai_step = min(
            st.session_state.ai_step + 1, len(path) - 1
        )

        if path[st.session_state.ai_step] == GOAL:
            st.session_state.finished = True
            st.session_state.message = "🤖 AI wins!"

def show_maze():
    player = st.session_state.player
    ai = path[st.session_state.ai_step]

    for r in range(ROWS):
        cells = []
        for c in range(COLS):
            pos = (r, c)

            if pos == player and pos == ai:
                cell = "⚔️"
            elif pos == player:
                cell = "🧍"
            elif pos == ai:
                cell = "🤖"
            elif pos == START:
                cell = "🟢"
            elif pos == GOAL:
                cell = "🏁"
            elif maze[r][c] == '#':
                cell = "⬛"
            else:
                cell = "⬜"

            cells.append(cell)

        st.write(" ".join(cells))

st.subheader("Maze")
show_maze()

st.caption("🧍 You | 🤖 AI | ⬛ Wall | 🏁 Goal")

st.subheader("Your Controls")

col1, col2, col3 = st.columns(3)

with col1:
    st.button("⬅️ Left", on_click=move_player, args=(0, -1),
              disabled=st.session_state.finished)

with col2:
    st.button("⬆️ Up", on_click=move_player, args=(-1, 0),
              disabled=st.session_state.finished)
    st.button("⬇️ Down", on_click=move_player, args=(1, 0),
              disabled=st.session_state.finished)

with col3:
    st.button("➡️ Right", on_click=move_player, args=(0, 1),
              disabled=st.session_state.finished)

st.button("🔄 Restart Game", on_click=reset_game)

if st.session_state.message:
    st.success(st.session_state.message)

st.write("**Challenge:** Reach 🏁 before the AI!")
