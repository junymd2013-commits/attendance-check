# 出席確認プログラム（UTF-8 / cp932 どちらでも読める安全版）

import streamlit as st
import pandas as pd
import datetime
import os

# タイトル
st.title("学籍番号 → 氏名照合システム")

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

    # ③ どちらも失敗した場合
    st.error("名簿ファイル（meibo_1.csv）の文字コードを判定できませんでした。UTF-8 または Shift-JIS で保存してください。")
    return pd.DataFrame(columns=["id", "name"])

df = load_data()

# 入力欄
student_id = st.text_input("学籍番号を入力してください", max_chars=10)

# attendance.csv が存在する場合だけ読み込む関数
def load_attendance():
    if os.path.exists("attendance.csv"):
        return pd.read_csv("attendance.csv", encoding="cp932", names=["id", "name", "time"])
    else:
        return pd.DataFrame(columns=["id", "name", "time"])

# 照合処理
if student_id:
    hit = df[df["id"] == student_id]
    if len(hit) == 1:
        name = hit.iloc[0]["name"]
        st.success(f"あなたの名前：**{name}** さん")

        # 出席ボタン
        if st.button("出席する"):
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            with open("attendance.csv", "a", encoding="cp932") as f:
                f.write(f"{student_id},{name},{now}\n")
            st.info("出席を記録しました")

        # 出席データの読み込み
        attendance_df = load_attendance()

        # ダウンロード用CSV（BOM付き Shift-JIS）
        csv = attendance_df.to_csv(index=False, encoding="cp932", errors="ignore")
        csv = "\ufeff" + csv  # Excel で文字化けしないための BOM 付与

        st.download_button(
            label="出欠データをダウンロード（attendance.csv）",
            data=csv,
            file_name="attendance.csv",
            mime="text/csv"
        )

    else:
        st.error("学籍番号が見つかりません")
