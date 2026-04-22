import streamlit as st
import pandas as pd

# タイトル
st.title("学籍番号 → 氏名照合システム")

# 名簿CSVの読み込み
@st.cache_data
def load_data():
# ← ここを修正（encoding="cp932"）
     df = pd.read_csv("meibo_1.csv", dtype={"id": str}, encoding="cp932")
#    df = pd.read_csv("meibo_1.csv", dtype={"id": str}, encoding="utf-8")

#    df = pd.read_csv("meibo.csv", dtype={"id": str})
    return df

df = load_data()

# 入力欄
student_id = st.text_input("学籍番号を入力してください", max_chars=10)

# 照合処理
if student_id:
    hit = df[df["id"] == student_id]

    if len(hit) == 1:
        name = hit.iloc[0]["name"]
        st.success(f"あなたの名前：**{name}** さん")

        # 出席ボタン
        if st.button("出席する"):
            # 出席記録を保存（CSVに追記）
            import datetime
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            with open("attendance.csv", "a", encoding="utf-8") as f:
                f.write(f"{student_id},{name},{now}\n")

            st.info("出席を記録しました")
    else:
        st.error("学籍番号が見つかりません")
