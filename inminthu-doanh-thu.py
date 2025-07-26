import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import matplotlib.pyplot as plt

st.set_page_config(layout="wide")
st.title("📊 Ghi nhận doanh thu - INMINHTHU CAFÉ")

# --- Khởi tạo session state ---
if "data" not in st.session_state:
    st.session_state["data"] = []

# --- Nhập thông tin ---
col1, col2, col3, col4, col5 = st.columns(5)
with col1:
    ngay = st.date_input("Chọn ngày", value=date.today(), format="DD/MM/YYYY")
with col2:
    thoi_gian = st.time_input("Chọn giờ phút", value=datetime.now().time())
with col3:
    khach_hang = st.text_input("Tên khách hàng")
with col4:
    loai = st.selectbox("Loại nước", ["Cà phê đen", "Cà phê sữa", "Cà phê muối", "Bạc xỉu", "Trà tắc", "Trà đường", "Matcha muối"])
with col5:
    kich_co = st.selectbox("Size", ["M 500ml", "L 800ml", "XL 1 lít"])

# --- Nhấn nút thêm ---
if st.button("➕ Thêm vào danh sách"):
    timestamp = datetime.combine(ngay, thoi_gian)
    st.session_state["data"].append({
        "Thời gian": timestamp,
        "Khách hàng": khach_hang,
        "Loại": loai,
        "Size": kich_co
    })

# --- Hiển thị bảng dữ liệu ---
data = pd.DataFrame(st.session_state["data"])
if not data.empty:
    st.subheader("📋 Danh sách khách hàng theo từng ngày")
    data_sorted = data.sort_values("Thời gian")
    st.dataframe(data_sorted, use_container_width=True)

    # --- Tính tổng số ly mỗi ngày ---
    data["Ngày"] = data["Thời gian"].dt.date
    ly_moi_ngay = data.groupby("Ngày").size().reset_index(name="Tổng số ly")
    st.subheader("📅 Số ly bán mỗi ngày")
    st.dataframe(ly_moi_ngay, use_container_width=True)

    # --- Loại nước bán nhiều nhất mỗi ngày ---
    top_loai = data.groupby(["Ngày", "Loại"]).size().reset_index(name="Số lượng")
    idx = top_loai.groupby("Ngày")["Số lượng"].idxmax()
    best_seller = top_loai.loc[idx].reset_index(drop=True)
    st.subheader("🏆 Loại nước bán nhiều nhất mỗi ngày")
    st.dataframe(best_seller, use_container_width=True)

    # --- Biểu đồ loại nước bán chạy ---
    st.subheader("📈 Biểu đồ số lượng bán theo loại")
    loai_chart = data["Loại"].value_counts()
    fig, ax = plt.subplots()
    loai_chart.plot(kind="bar", ax=ax, color="skyblue")
    ax.set_ylabel("Số lượng")
    ax.set_title("Tổng số lượng bán theo loại nước")
    st.pyplot(fig)
