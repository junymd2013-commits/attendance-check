# 1_学生用ページ.py
import streamlit as st
import pandas as pd
import datetime
import os

st.title("学生用：出席入力ページ")

# 名簿CSVの読み込み（UTF-8 → cp932 の順で試す）
@st.cache_data
def load_data():
    file = "meibo_1.csv"

    # ① UTF-8 で読み込みを試す
    try:
        df = pd.read_csv(file, dtype={"id": str}, encoding="utf-8")
        return df
    except Exception:
        pass

    # ② cp932（Shift-JIS）で読み込みを試す
    try:
        df = pd.read_csv(file, dtype={"id": str}, encoding="cp932")
        return df
    except Exception:
        pass

    st.error("名簿ファイル（meibo_1.csv）を読み込めませんでした。文字コードを UTF-8 または Shift-JIS にしてください。")
    return pd.DataFrame(columns=["id", "name"])

df = load_data()

# 入力欄
student_id = st.text_input("学籍番号を入力してください", max_chars=10)

# 出席記録ファイルのパス
ATTEND_FILE = "attendance.csv"

# 出席ボタンと処理
if student_id:
    hit = df[df["id"] == student_id]
    if len(hit) == 1:
        name = hit.iloc[0]["name"]
        st.success(f"あなたの名前：**{name}** さん")

        if st.button("出席する"):
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # 出席を追記（cp932 で保存）
            with open(ATTEND_FILE, "a", encoding="cp932") as f:
                f.write(f"{student_id},{name},{now}\n")
            st.info("出席を記録しました。画面を閉じてかまいません。")
    else:
        st.error("学籍番号が名簿に見つかりません。もう一度確認してください。")
