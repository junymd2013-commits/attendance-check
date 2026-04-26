import streamlit as st
import pandas as pd
import os

st.title("教員用：出席一覧確認ページ")

# attendance.csv の読み込み
def load_attendance():
    if os.path.exists("attendance.csv"):
        return pd.read_csv("attendance.csv", encoding="cp932", names=["id", "name", "time"])
    else:
        st.warning("attendance.csv がまだありません。学生が出席すると自動生成されます。")
        return pd.DataFrame(columns=["id", "name", "time"])

attendance_df = load_attendance()

# データがある場合のみ表示
if len(attendance_df) > 0:

    # ID順に並べ替え
    attendance_sorted = attendance_df.sort_values("id")

    st.subheader("出席一覧（ID順）")
    st.dataframe(attendance_sorted, use_container_width=True)

    # ダウンロード（BOM付き Shift-JIS）
    csv = attendance_sorted.to_csv(index=False, encoding="cp932", errors="ignore")
    csv = "\ufeff" + csv

    st.download_button(
        label="出席一覧をダウンロード（attendance.csv）",
        data=csv,
        file_name="attendance_sorted.csv",
        mime="text/csv"
    )
else:
    st.info("まだ出席データがありません。")
