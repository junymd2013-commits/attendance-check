import streamlit as st
import random
import math

# -----------------------------
# ユークリッドの互除法の途中式を生成
# -----------------------------
def euclid_steps(a, b):
    steps = []
    while b != 0:
        q = a // b
        r = a % b
        steps.append(f"{a} = {b} × {q} + {r}")
        a, b = b, r
    steps.append(f"最大公約数 = {a}")
    return steps

# -----------------------------
# 初級：目算しやすい問題生成
# -----------------------------
def generate_easy_problem():
    while True:
        # 目算しやすい数を優先
        a = random.choice([
            random.randint(20, 99),
            random.randrange(20, 200, 5),
            random.randrange(20, 200, 10)
        ])
        b = random.choice([
            random.randint(20, 99),
            random.randrange(20, 200, 5),
            random.randrange(20, 200, 10)
        ])

        # gcd が 1 になりにくいように調整
        if math.gcd(a, b) >= 2:
            return (a, b)

# -----------------------------
# 中級：3桁以内、gcd >= 3
# -----------------------------
def generate_middle_problem():
    while True:
        a = random.randint(100, 999)
        b = random.randint(100, 999)
        if math.gcd(a, b) >= 3:
            return (a, b)

# -----------------------------
# 上級：4桁 × 3桁、gcd >= 6
# -----------------------------
def generate_hard_problem():
    while True:
        a = random.randint(1000, 9999)
        b = random.randint(100, 999)
        if math.gcd(a, b) >= 6:
            return (a, b)

# -----------------------------
# 難易度ごとの問題生成
# -----------------------------
def generate_problems(level):
    problems = []
    used = set()

    while len(problems) < 5:
        if level == 1:
            p = generate_easy_problem()
        elif level == 2:
            p = generate_middle_problem()
        else:
            p = generate_hard_problem()

        if p not in used:
            used.add(p)
            problems.append(p)

    return problems

# -----------------------------
# Streamlit UI
# -----------------------------
st.title("最大公約数（GCD）5題セット（難易度つき）")

level = st.radio(
    "難易度を選択してください",
    [1, 2, 3],
    format_func=lambda x: {1: "★1（初級：目算中心）", 2: "★2（中級）", 3: "★3（上級：途中式表示）"}[x]
)

if "problems" not in st.session_state:
    st.session_state.problems = []
if "answer_keys" not in st.session_state:
    st.session_state.answer_keys = []

if st.button("新しい問題を生成する"):
    st.session_state.problems = generate_problems(level)
    st.session_state.answer_keys = [f"ans_{random.randint(1, 10**9)}" for _ in range(5)]

if not st.session_state.problems:
    st.stop()

problems = st.session_state.problems
answer_keys = st.session_state.answer_keys

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

if st.button("採点する"):
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

        # ★3 のときは途中式を表示
        if level == 3:
            st.write("【ユークリッドの互除法の途中式】")
            for step in euclid_steps(a, b):
                st.write(step)

    st.write(f"### 合計得点：**{score} / 5**")

    # -----------------------------
    # 数学B向けの丁寧な解説
    # -----------------------------
    st.subheader("【解説：数学Bで学ぶユークリッドの互除法】")
    st.write("""
ユークリッドの互除法は、2つの整数 a, b の最大公約数を求めるための最も基本的で強力な方法です。

### ■ なぜ互除法で最大公約数が求まるのか
a を b で割った余りを r とすると  
**gcd(a, b) = gcd(b, r)**  
が成り立ちます。

理由は、a と b の共通の約数は、a - b×q（＝余り r）も割り切るためです。

### ■ 手順
1. a を b で割り、余り r を求める  
2. (a, b) を (b, r) に置き換える  
3. r = 0 になったときの b が最大公約数  

この方法は、整数の性質に基づく非常に重要なアルゴリズムで、数学Bの「整数の性質」の中心的内容です。
""")
