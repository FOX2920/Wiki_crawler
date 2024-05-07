import streamlit as st
from demo import main as demo_main
from crawler import main as crawler_main

# Thiết lập layout
st.set_page_config(layout="wide")

# Lựa chọn trang
page = st.sidebar.selectbox("Chọn trang", ["Demo", "Crawler"])

# Hiển thị trang tương ứng dựa trên lựa chọn
if page == "Demo":
    demo_main()
elif page == "Crawler":
    crawler_main()
