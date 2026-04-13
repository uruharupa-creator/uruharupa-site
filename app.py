import streamlit as st

st.set_page_config(page_title="Task Pet App", page_icon="🐣", layout="centered")

if "tasks" not in st.session_state:
    st.session_state.tasks = []

if "points" not in st.session_state:
    st.session_state.points = 0

if "combo" not in st.session_state:
    st.session_state.combo = 0

if "next_id" not in st.session_state:
    st.session_state.next_id = 1

def get_pet_stage(points):
    if points >= 50:
        return "🐔 ニワトリ"
    elif points >= 20:
        return "🐤 ヒヨコ"
    else:
        return "🥚 たまご"

def get_message(points):
    if points >= 50:
        return "すごい！かなり育ってきたね！"
    elif points >= 20:
        return "いい感じに進んでるよ！"
    else:
        return "小さな1歩、えらい！"

def add_task(task_text):
    task_text = task_text.strip()
    if not task_text:
        return
    st.session_state.tasks.append({"id": st.session_state.next_id, "text": task_text})
    st.session_state.next_id += 1

def complete_task(task_id):
    for i, task in enumerate(st.session_state.tasks):
        if task["id"] == task_id:
            completed_task = st.session_state.tasks.pop(i)
            st.session_state.points += 10
            st.session_state.combo += 1

            st.success(f"『{completed_task['text']}』を完了したよ！ +10pt")

            if st.session_state.combo >= 3:
                st.session_state.points += 20
                st.session_state.combo = 0
                st.info("3回連続達成ボーナス！ +20pt")
            return

st.title("🫧 ADHD向け タスク育成アプリ")

pet_stage = get_pet_stage(st.session_state.points)

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🐾 状態")
    st.metric("ポイント", f"{st.session_state.points} pt")
    st.metric("コンボ", st.session_state.combo)
    st.markdown(f"### {pet_stage}")
    st.write(get_message(st.session_state.points))

with col2:
    st.subheader("➕ タスク追加")
    new_task = st.text_input("やること")
    if st.button("追加"):
        add_task(new_task)
        st.rerun()

st.divider()

st.subheader("📋 タスク")

for task in st.session_state.tasks:
    col1, col2 = st.columns([4, 1])
    with col1:
        st.write(task["text"])
    with col2:
        if st.button("完了", key=task["id"]):
            complete_task(task["id"])
            st.rerun()