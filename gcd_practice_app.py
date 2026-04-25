import streamlit as st
import random
import math

# -----------------------------
# セッション状態の初期化
# -----------------------------
if "problems" not in st.session_state:
    st.session_state.problems = []
if "answer_keys" not in st.session_state:
    st.session_state.answer_keys = []  # 解答欄の key を管理

st.title("最大公約数（GCD）5題セット")
st.write("5題の最大公約数を求めてください。採点後は新しい問題に進めます。")

# -----------------------------
# 問題生成
# -----------------------------
def generate_problems():
    problems = []
    for _ in range(5):
        a = random.randint(20, 200)
        b = random.randint(20, 200)
        problems.append((a, b))
    return problems

# -----------------------------
# 新しい問題を生成（解答欄リセット）
# -----------------------------
if st.button("新しい問題を生成する", key="generate"):
    st.session_state.problems = generate_problems()

    # 解答欄の key を毎回リセット
    st.session_state.answer_keys = [f"ans_{random.randint(1, 10**9)}" for _ in range(5)]

# 初回は問題なし
if not st.session_state.problems:
    st.stop()

problems = st.session_state.problems

# -----------------------------
# 解答欄の key が未生成なら作る
# -----------------------------
if not st.session_state.answer_keys:
    st.session_state.answer_keys = [f"ans_{random.randint(1, 10**9)}" for _ in range(5)]

answer_keys = st.session_state.answer_keys

# -----------------------------
# 問題表示 & 解答入力
# -----------------------------
st.subheader("【問題】最大公約数を求めなさい")

user_answers = []
for i, (a, b) in enumerate(problems):
    st.write(f"**第 {i+1} 問：gcd({a}, {b}) を求めよ**")
    ans = st.number_input(
        f"あなたの解答（第 {i+1} 問）",
        key=answer_keys[i],
        step=1
    )
    user_answers.append(ans)

# -----------------------------
# 採点
# -----------------------------
if st.button("採点する", key="grade"):
    st.subheader("【採点結果】")
    score = 0

    for i, (a, b) in enumerate(problems):
        correct = math.gcd(a, b)
        user_ans = user_answers[i]

        if user_ans == correct:
            st.success(f"第 {i+1} 問：正解！ → {correct}")
            score += 1
        else:
            st.error(f"第 {i+1} 問：不正解。あなたの答え = {user_ans}、正解 = {correct}")

    st.write(f"### 合計得点：**{score} / 5**")

    st.subheader("【解説：ユークリッドの互除法】")
    st.write("""
gcd(a, b) は次の手順で求められます：

1. a を b で割った余り r を求める  
2. gcd(a, b) = gcd(b, r)  
3. r = 0 になったときの b が最大公約数  

例：gcd(84, 30)  
- 84 ÷ 30 = 2 余り 24 → gcd(30, 24)  
- 30 ÷ 24 = 1 余り 6 → gcd(24, 6)  
- 24 ÷ 6 = 4 余り 0 → **最大公約数は 6**
""")
