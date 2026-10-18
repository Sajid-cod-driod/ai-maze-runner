import streamlit as st
from collections import deque

st.set_page_config(page_title="AI Maze Runner", page_icon="🎮")

st.title("🎮 AI Maze Runner")
st.write("Can you reach the goal before the AI?")

# Three levels
MAZES = {
    1: [
        "S#......",
        ".#.###..",
        ".....#..",
        "####.#..",
        "........",
        ".######.",
        "......#.",
        ".####..G",
    ],
    2: [
        "S...#...",
        "##..#.#.",
        "...##.#.",
        ".#....#.",
        ".#.####.",
        ".#......",
        "...####.",
        "......#G",
    ],
    3: [
        "S.......",
        ".######.",
        "......#.",
        "#####.#.",
        "......#.",
        ".######.",
        "........",
        "#######G",
    ],
}

LEVEL_NAMES = {1: "Easy", 2: "Medium", 3: "Hard"}

def get_start_goal(maze):
    start = goal = None
    for r, row in enumerate(maze):
        for c, cell in enumerate(row):
            if cell == "S":
                start = (r, c)
            elif cell == "G":
                goal = (r, c)
    return start, goal

def find_path(maze):
    start, goal = get_start_goal(maze)
    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        (r, c), path = queue.popleft()

        if (r, c) == goal:
            return path

        for dr, dc in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            nr, nc = r + dr, c + dc

            if (
                0 <= nr < len(maze)
                and 0 <= nc < len(maze[0])
                and maze[nr][nc] != "#"
                and (nr, nc) not in visited
            ):
                visited.add((nr, nc))
                queue.append(((nr, nc), path + [(nr, nc)]))

    return []

# Game state
if "level" not in st.session_state:
    st.session_state.level = 1
    st.session_state.unlocked_level = 1
    st.session_state.score = 0
    st.session_state.wins = 0
    st.session_state.player = (0, 0)
    st.session_state.ai_step = 0
    st.session_state.finished = False
    st.session_state.message = ""

level = st.session_state.level
maze = MAZES[level]
path = find_path(maze)
start, goal = get_start_goal(maze)

# Correct player position when level changes
if "current_level" not in st.session_state:
    st.session_state.current_level = level

if st.session_state.current_level != level:
    st.session_state.current_level = level
    st.session_state.player = start
    st.session_state.ai_step = 0
    st.session_state.finished = False
    st.session_state.message = ""

if not path:
    st.error("This maze has no solution. Please check the maze layout.")
    st.stop()

st.subheader(f"Level {level}: {LEVEL_NAMES[level]}")

# Scoreboard
a, b, c = st.columns(3)
a.metric("⭐ Your Score", st.session_state.score)
b.metric("🏆 Levels Won", st.session_state.wins)
c.metric("🤖 AI Progress", f"{st.session_state.ai_step}/{len(path)-1}")

st.write(f"🔓 Highest unlocked level: {st.session_state.unlocked_level}")

def restart_level():
    st.session_state.player = get_start_goal(
        MAZES[st.session_state.level]
    )[0]
    st.session_state.ai_step = 0
    st.session_state.finished = False
    st.session_state.message = ""

def next_level():
    if st.session_state.level < 3:
        st.session_state.level += 1
        st.session_state.player = get_start_goal(
            MAZES[st.session_state.level]
        )[0]
        st.session_state.ai_step = 0
        st.session_state.finished = False
        st.session_state.message = ""

def move_player(dr, dc):
    if st.session_state.finished:
        return

    r, c = st.session_state.player
    nr, nc = r + dr, c + dc
    current_maze = MAZES[st.session_state.level]

    # Move only if the next cell is free
    if (
        0 <= nr < len(current_maze)
        and 0 <= nc < len(current_maze[0])
        and current_maze[nr][nc] != "#"
    ):
        st.session_state.player = (nr, nc)

    # Check if the player won
    current_start, current_goal = get_start_goal(current_maze)

    if st.session_state.player == current_goal:
        st.session_state.finished = True
        st.session_state.message = "win"
        st.session_state.score += 100
        st.session_state.wins += 1
        st.session_state.unlocked_level = max(
            st.session_state.unlocked_level,
            min(st.session_state.level + 1, 3)
        )
        return

    # AI advances one step per player move
    current_path = find_path(current_maze)
    st.session_state.ai_step = min(
        st.session_state.ai_step + 1, len(current_path) - 1
    )

    if current_path[st.session_state.ai_step] == current_goal:
        st.session_state.finished = True
        st.session_state.message = "ai"

def show_maze():
    player = st.session_state.player
    ai_position = path[st.session_state.ai_step]

    for r in range(len(maze)):
        cells = []

        for c in range(len(maze[0])):
            pos = (r, c)

            if pos == player and pos == ai_position:
                cell = "⚔️"
            elif pos == player:
                cell = "🧍"
            elif pos == ai_position:
                cell = "🤖"
            elif maze[r][c] == "S":
                cell = "🟢"
            elif maze[r][c] == "G":
                cell = "🏁"
            elif maze[r][c] == "#":
                cell = "⬛"
            else:
                cell = "⬜"

            cells.append(cell)

        st.write(" ".join(cells))

show_maze()

st.caption("🧍 You | 🤖 AI | ⬛ Wall | 🏁 Goal")

st.subheader("🎮 Your Controls")

col1, col2, col3 = st.columns(3)

with col1:
    st.button(
        "⬅️ Left",
        on_click=move_player,
        args=(0, -1),
        disabled=st.session_state.finished
    )

with col2:
    st.button(
        "⬆️ Up",
        on_click=move_player,
        args=(-1, 0),
        disabled=st.session_state.finished
    )
    st.button(
        "⬇️ Down",
        on_click=move_player,
        args=(1, 0),
        disabled=st.session_state.finished
    )

with col3:
    st.button(
        "➡️ Right",
        on_click=move_player,
        args=(0, 1),
        disabled=st.session_state.finished
    )

st.button("🔄 Restart Level", on_click=restart_level)

if st.session_state.message == "win":
    if level < 3:
        st.success(f"🏆 You won Level {level}! +100 points. Level {level + 1} unlocked!")
        st.button("➡️ Next Level", on_click=next_level)
    else:
        st.balloons()
        st.success("🎉 Congratulations! You completed all 3 levels!")
elif st.session_state.message == "ai":
    st.error("🤖 AI reached the goal first! Restart this level and try again.")
