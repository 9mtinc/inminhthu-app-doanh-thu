import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Thiết lập tiêu đề
st.title("INMINHTHU CAFÉ - QUẢN LÝ DOANH THU")

# Dữ liệu menu
menu = {
    "Cà phê đen": {"M": 12_000, "L": 17_000, "XL": 20_000},
    "Cà phê sữa": {"M": 15_000, "L": 19_000, "XL": 23_000},
    "Cà phê muối": {"M": 16_000, "L": 21_000, "XL": 26_000},
    "Bạc xỉu": {"M": 17_000, "L": 22_000, "XL": 27_000},
    "Trà tắc": {"M": 8_000, "L": 10_000, "XL": 15_000},
    "Trà đường": {"M": 6_000, "L": 9_000, "XL": 10_000},
    "Matcha latte": {"M": 17_000, "L": 22_000, "XL": 26_000},
    "Matcha kem cheese": {"M": 20_000, "L": 26_000, "XL": 30_000}
}

# Giá vốn ước tính (có thể chỉnh theo thực tế)
von = {
    "Cà phê đen": 5_000, "Cà phê sữa": 6_000, "Cà phê muối": 6_000, "Bạc xỉu": 6_000,
    "Trà tắc": 3_000, "Trà đường": 2_000, "Matcha latte": 8_000, "Matcha kem cheese": 10_000
}

# Nhập thông tin
with st.form("form"):
    customer = st.text_input("Tên khách hàng")
    date_time = st.datetime_input("Chọn ngày giờ")

    selections = []
    for i in range(1, 6):
        with st.expander(f"Đồ uống {i}"):
            drink = st.selectbox(f"Chọn món {i}", [""] + list(menu.keys()), key=f"drink_{i}")
            if drink:
                size = st.selectbox("Chọn size", ["M", "L", "XL"], key=f"size_{i}")
                qty = st.number_input("Số lượng", min_value=1, value=1, step=1, key=f"qty_{i}")
                selections.append({"drink": drink, "size": size, "qty": qty})

    submitted = st.form_submit_button("Thêm đơn hàng")

# Khởi tạo session state
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(columns=["Thời gian", "Khách", "Món", "Size", "SL", "Đơn giá", "Doanh thu", "Chi phí", "Lợi nhuận"])

# Xử lý dữ liệu đơn hàng
if submitted and customer and selections:
    for sel in selections:
        drink = sel["drink"]
        size = sel["size"]
        qty = sel["qty"]
        price = menu[drink][size]
        cost = von[drink]
        total_revenue = price * qty
        total_cost = cost * qty
        profit = total_revenue - total_cost

        new_row = pd.DataFrame({
            "Thời gian": [date_time.strftime("%Y-%m-%d %H:%M")],
            "Khách": [customer],
            "Món": [drink],
            "Size": [size],
            "SL": [qty],
            "Đơn giá": [price],
            "Doanh thu": [total_revenue],
            "Chi phí": [total_cost],
            "Lợi nhuận": [profit]
        })
        st.session_state.data = pd.concat([st.session_state.data, new_row], ignore_index=True)
    st.success("Đã thêm đơn hàng")

# Hiển thị bảng dữ liệu
st.subheader("📋 Danh sách đơn hàng")
st.dataframe(st.session_state.data, use_container_width=True)

# Tổng kết theo ngày
if not st.session_state.data.empty:
    st.subheader("📊 Tổng kết theo ngày")
    st.session_state.data["Ngày"] = pd.to_datetime(st.session_state.data["Thời gian"]).dt.date
    daily_summary = st.session_state.data.groupby("Ngày").agg({
        "SL": "sum",
        "Doanh thu": "sum",
        "Chi phí": "sum",
        "Lợi nhuận": "sum"
    }).reset_index()
    st.dataframe(daily_summary, use_container_width=True)

    # Vẽ biểu đồ
    st.subheader("📈 Biểu đồ doanh thu & lợi nhuận")
    fig, ax = plt.subplots()
    ax.plot(daily_summary["Ngày"], daily_summary["Doanh thu"], marker='o', label="Doanh thu")
    ax.plot(daily_summary["Ngày"], daily_summary["Lợi nhuận"], marker='s', label="Lợi nhuận")
    ax.set_xlabel("Ngày")
    ax.set_ylabel("VNĐ")
    ax.legend()
    st.pyplot(fig)
