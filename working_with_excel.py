import pandas as pd
import streamlit as st
#kartikay  gay hai 
st.set_page_config(layout="wide")

file_path = r"C:\Users\priya\OneDrive\Desktop\hack\qwerty.xlsx"
df = pd.read_excel(file_path)

# Parse date correctly (day first) and format as DD-MM-YYYY
df['date'] = pd.to_datetime(df['date'], dayfirst=True, errors='coerce').dt.strftime("%d-%m-%Y")

# Filters
col1, col2 = st.columns(2)

# Month filter
months = pd.to_datetime(df['date'], format="%d-%m-%Y", errors='coerce').dt.month.dropna().unique()
month_map = {1:"Jan", 2:"Feb", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun",
             7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}
month_names = [month_map[m] for m in sorted(months)]

selected_month = col1.selectbox("Filter by Month", ["All"] + month_names)

# Publishedby filter
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

# Show rows (10 or all)
if "show_all" not in st.session_state:
    st.session_state["show_all"] = False

display_df = filtered_df if st.session_state["show_all"] else filtered_df.head(10)

# Custom display with summary + link
for _, row in display_df.iterrows():
    with st.container():
        cols = st.columns([2, 2, 4, 2])  # adjust widths
        cols[0].write(row["date"])
        cols[1].write(row["noticeheadline"])
        cols[2].markdown(f"[Open Link](https://example.com)")  # replace with your link later

        # Dropdown/Expander for summary
        with st.expander("Summary"):
            st.write("Summary text here...")  # You will fill later

st.markdown("---")

if not st.session_state["show_all"]:
    if st.button("Show All"):
        st.session_state["show_all"] = True
