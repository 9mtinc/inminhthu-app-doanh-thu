# INMINHTHU CAFÉ - QUẢN LÝ DOANH THU

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

st.set_page_config(page_title="INMINHTHU CAFÉ - QUẢN LÝ DOANH THU", layout="wide")
st.title("INMINHTHU CAFÉ - QUẢN LÝ DOANH THU")

# --- Dữ liệu menu ---
menu = {
    "Cà phê đen": {"M": 12, "L": 17, "XL": 20, "cost": 3.5},
    "Cà phê sữa": {"M": 15, "L": 19, "XL": 23, "cost": 4.5},
    "Matcha muối": {"M": 17, "L": 22, "XL": 26, "cost": 6.0},
    "Bạc xỉu": {"M": 17, "L": 22, "XL": 27, "cost": 5.5},
    "Trà tắc": {"M": 8, "L": 10, "XL": 15, "cost": 3.0},
    "Trà đường": {"M": 6, "L": 9, "XL": 10, "cost": 2.5},
    "Matcha latte": {"M": 17, "L": 22, "XL": 26, "cost": 6.0},
}

# --- Khởi tạo session ---
if "sales" not in st.session_state:
    st.session_state.sales = []

# --- Nhập dữ liệu ---
st.subheader("Nhập giao dịch")
col1, col2 = st.columns(2)

with col1:
    customer = st.text_input("Tên khách hàng")
    date_time = st.datetime_input("Chọn ngày giờ", format="%A - %d/%m/%Y %H:%M")
with col2:
    drink = st.selectbox("Chọn đồ uống", list(menu.keys()))
    size = st.radio("Size", ["M", "L", "XL"])
    quantity = st.number_input("Số ly", min_value=1, value=1)

if st.button("Lưu giao dịch"):
    price = menu[drink][size]
    cost = menu[drink]["cost"]
    total_cost = cost * quantity
    total_price = price * quantity
    profit = total_price - total_cost

    st.session_state.sales.append({
        "Thời gian": date_time,
        "Khách hàng": customer,
        "Món": drink,
        "Size": size,
        "Số ly": quantity,
        "Doanh thu": total_price,
        "Chi phí": total_cost,
        "Lợi nhuận": profit
    })
    st.success("Đã lưu giao dịch!")

# --- Hiển thị dữ liệu ---
st.subheader("Bảng doanh thu")
df = pd.DataFrame(st.session_state.sales)
if not df.empty:
    df_sorted = df.sort_values(by="Thời gian", ascending=False)
    st.dataframe(df_sorted, use_container_width=True)

    # --- Thống kê theo ngày ---
    df["Ngày"] = df["Thời gian"].dt.date
    grouped = df.groupby("Ngày").agg({
        "Số ly": "sum",
        "Doanh thu": "sum",
        "Chi phí": "sum",
        "Lợi nhuận": "sum"
    }).reset_index()

    st.subheader("Tổng hợp theo ngày")
    st.dataframe(grouped, use_container_width=True)

    # --- Biểu đồ doanh thu ---
    st.subheader("Biểu đồ doanh thu theo ngày")
    fig, ax = plt.subplots()
    ax.plot(grouped["Ngày"], grouped["Doanh thu"], marker="o", label="Doanh thu")
    ax.plot(grouped["Ngày"], grouped["Lợi nhuận"], marker="x", label="Lợi nhuận", linestyle="--")
    ax.set_xlabel("Ngày")
    ax.set_ylabel("Số tiền (nghìn đồng)")
    ax.legend()
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # --- Món bán chạy theo ngày ---
    st.subheader("Món bán chạy nhất theo ngày")
    top_items = df.groupby(["Ngày", "Món"])["Số ly"].sum().reset_index()
    idx = top_items.groupby("Ngày")["Số ly"].idxmax()
    st.dataframe(top_items.loc[idx].reset_index(drop=True), use_container_width=True)

    # --- Danh sách khách hàng theo ngày ---
    st.subheader("Danh sách khách hàng theo ngày")
    grouped_customers = df.groupby("Ngày")["Khách hàng"].apply(list).reset_index()
    st.dataframe(grouped_customers, use_container_width=True)
else:
    st.info("Chưa có giao dịch nào.")
