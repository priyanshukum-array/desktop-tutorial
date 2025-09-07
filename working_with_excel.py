import pandas as pd
import streamlit as st

st.set_page_config(layout="wide")

file_path = "qwerty.xlsx"
df = pd.read_excel(file_path)

df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce').dt.strftime("%d-%m-%Y")

# Drop rows where both date and headline are NaN
df = df.dropna(subset=["date", "noticeheadline"], how="all")

col1, col2 = st.columns(2)

months = pd.to_datetime(df['date'], format="%d-%m-%Y", errors='coerce').dt.month.dropna().astype(int).unique()
month_map = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}
month_names = [month_map[m] for m in sorted(months)]

selected_month = col1.selectbox("Filter by Month", ["All"] + month_names)
publishers = df['publishedby'].dropna().unique()
selected_publisher = col2.selectbox("Filter by Published By", ["All"] + sorted(publishers.tolist()))

filtered_df = df.copy()

if selected_month != "All":
    month_num = list(month_map.keys())[list(month_map.values()).index(selected_month)]
    filtered_df = filtered_df[
        pd.to_datetime(filtered_df['date'], format="%d-%m-%Y", dayfirst=True, errors='coerce').dt.month == month_num
    ]

if selected_publisher != "All":
    filtered_df = filtered_df[filtered_df['publishedby'] == selected_publisher]

if "show_all" not in st.session_state:
    st.session_state["show_all"] = False

display_df = filtered_df if st.session_state["show_all"] else filtered_df.head(10)

# Table style view
st.markdown("### Notices")
for _, row in display_df.iterrows():
    date = "" if pd.isna(row["date"]) else row["date"]
    headline = "" if pd.isna(row["noticeheadline"]) else row["noticeheadline"]
    publisher = "" if pd.isna(row["publishedby"]) else row["publishedby"]
    link = row.get("link", "https://example.com")

    cols = st.columns([2, 6, 3, 1])
    cols[0].write(date)
    cols[1].write(headline)
    cols[2].write(publisher)
    cols[3].markdown(f"[🔗]({link})")

st.markdown("---")

if not st.session_state["show_all"]:
    if st.button("Show All"):
        st.session_state["show_all"] = True
