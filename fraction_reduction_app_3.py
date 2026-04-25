import streamlit as st
import random
from fractions import Fraction
import math

# -----------------------------
# セッション状態の初期化
# -----------------------------
if "problems" not in st.session_state:
    st.session_state.problems = []
if "answer_keys" not in st.session_state:
    st.session_state.answer_keys = []

st.title("分数 → 既約分数に直す 5題セット")
st.write("難易度を選んで、5題の分数を既約分数に直しましょう。")

# -----------------------------
# 難易度設定
# -----------------------------
difficulty = st.radio(
    "難易度を選んでください。★1は既約の場合もあります。",
    ["★1（やさしい）", "★2（ふつう）", "★3（むずかしい）"]
)

# -----------------------------
# 問題生成関数
# -----------------------------
def generate_fraction(level):

    # ★1：小さめ
    if level == 1:
        num = random.randint(5, 50)
        den = random.randint(2, 30)

    # ★2：分子3桁まで、分母2桁まで、gcd >= 3
    elif level == 2:
        while True:
            num = random.randint(10, 999)   # 3桁まで
            den = random.randint(10, 99)    # 2桁まで
            if math.gcd(num, den) >= 3:
                break

    # ★3：分子4桁まで、分母3桁まで、gcd >= 6
    else:
        while True:
            num = random.randint(100, 9999)  # 4桁まで
            den = random.randint(100, 999)   # 3桁まで
            if math.gcd(num, den) >= 6:
                break

    if num == den:
        num += 1

    return num, den

# -----------------------------
# 重複なしで5題生成
# -----------------------------
def generate_problems(level):
    problems = set()
    while len(problems) < 5:
        problems.add(generate_fraction(level))
    return list(problems)

# -----------------------------
# 新しい問題を生成（解答欄リセット）
# -----------------------------
if st.button("問題を生成する", key="generate"):
    level = 1 if "★1" in difficulty else 2 if "★2" in difficulty else 3
    st.session_state.problems = generate_problems(level)

    # 解答欄の key を毎回ランダムに生成
    st.session_state.answer_keys = [
        f"ans_{random.randint(1, 10**9)}" for _ in range(5)
    ]

problems = st.session_state.problems

# 問題がまだないときは終了
if not problems:
    st.stop()

# -----------------------------
# 解答欄 key が未生成なら作る
# -----------------------------
if not st.session_state.answer_keys:
    st.session_state.answer_keys = [
        f"ans_{random.randint(1, 10**9)}" for _ in range(5)
    ]

answer_keys = st.session_state.answer_keys

# -----------------------------
# 問題表示 & 解答入力
# -----------------------------
st.subheader("【問題】次の分数を既約分数に直しなさい")

user_answers = []
for i, (num, den) in enumerate(problems):
    st.write(f"**第 {i+1} 問：  {num} / {den} を既約分数にせよ**")
    col1, col2 = st.columns(2)
    with col1:
        ans_num = st.number_input(
            f"分子（第{i+1}問）",
            key=answer_keys[i] + "_num",
            step=1
        )
    with col2:
        ans_den = st.number_input(
            f"分母（第{i+1}問）",
            key=answer_keys[i] + "_den",
            step=1
        )
    user_answers.append((ans_num, ans_den))

# -----------------------------
# 採点
# -----------------------------
if st.button("採点する", key="grade"):
    st.subheader("【採点結果】")
    score = 0

    for i, (num, den) in enumerate(problems):
        correct_frac = Fraction(num, den)
        user_num, user_den = user_answers[i]

        try:
            user_frac = Fraction(int(user_num), int(user_den))
            if user_frac == correct_frac:
                st.success(f"第 {i+1} 問：正解！ → {correct_frac}")
                score += 1
            else:
                st.error(
                    f"第 {i+1} 問：不正解。あなたの答え = {user_num}/{user_den}、正解 = {correct_frac}"
                )
        except Exception:
            st.error(f"第 {i+1} 問：入力エラー（整数で入力してください）")

    st.write(f"### 合計得点：**{score} / 5**")

    st.subheader("【解説：既約分数の求め方】")
    st.write(
        "分数 a/b を既約分数にするには、分子と分母の最大公約数（gcd）で割ります。\n\n"
        "例： 84/30\n"
        "- gcd(84, 30) = 6\n"
        "- 84 ÷ 6 = 14\n"
        "- 30 ÷ 6 = 5\n"
        "→ 14/5 が既約分数です。"
    )
