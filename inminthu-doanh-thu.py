import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from collections import defaultdict

st.set_page_config(page_title="INMINHTHU CAFÉ", layout="wide")

# Menu đồ uống và chi phí nguyên liệu
menu = {
    "Cà phê đen": {"M": 12, "L": 17, "XL": 20},
    "Cà phê sữa": {"M": 15, "L": 19, "XL": 23},
    "Cà phê muối": {"M": 16, "L": 21, "XL": 26},
    "Bạc xỉu": {"M": 17, "L": 22, "XL": 27},
    "Trà tắc": {"M": 8, "L": 10, "XL": 15},
    "Trà đường": {"M": 6, "L": 9, "XL": 10},
    "Matcha latte": {"M": 17, "L": 22, "XL": 26},
    "Matcha latte muối": {"M": 17, "L": 22, "XL": 26},
}

# Chi phí nguyên liệu mỗi ly (ước lượng)
chi_phi = {
    "Cà phê đen": 4,
    "Cà phê sữa": 6,
    "Cà phê muối": 7,
    "Bạc xỉu": 7,
    "Trà tắc": 3,
    "Trà đường": 2,
    "Matcha latte": 10,
    "Matcha latte muối": 11,
}

# Bộ nhớ tạm để lưu dữ liệu khách hàng theo ngày
if "data" not in st.session_state:
    st.session_state.data = defaultdict(list)

st.title("📊 INMINHTHU CAFÉ – Ghi nhận bán hàng")

# Lấy thời gian hiện tại
now = datetime.now()
date_str = now.strftime("%A, %d/%m/%Y")
time_str = now.strftime("%H:%M")
st.markdown(f"### 🗓️ {date_str} – 🕒 {time_str}")

st.markdown("---")

st.subheader("➕ Nhập đơn mới")
col1, col2, col3 = st.columns(3)

with col1:
    ten_khach = st.text_input("Tên khách hàng")

with col2:
    ten_mon = st.selectbox("Chọn món", list(menu.keys()))

with col3:
    size = st.radio("Chọn size", ["M", "L", "XL"], horizontal=True)

if st.button("✅ Thêm đơn"):
    if not ten_khach:
        st.warning("Vui lòng nhập tên khách hàng!")
    else:
        gia_ban = menu[ten_mon][size]
        phi = chi_phi[ten_mon]
        loi_nhuan = gia_ban - phi
        st.success(f"Đã thêm đơn cho {ten_khach}: {ten_mon} size {size} – Giá bán {gia_ban}k – Lợi nhuận {loi_nhuan}k")
        st.session_state.data[date_str].append({
            "Giờ": time_str,
            "Khách": ten_khach,
            "Món": ten_mon,
            "Size": size,
            "Giá bán": gia_ban,
            "Chi phí": phi,
            "Lợi nhuận": loi_nhuan
        })

st.markdown("---")

st.subheader("📋 Danh sách đơn trong ngày")

if date_str in st.session_state.data and st.session_state.data[date_str]:
    df = pd.DataFrame(st.session_state.data[date_str])
    st.dataframe(df, use_container_width=True)

    st.markdown("---")
    st.subheader("📊 Thống kê nhanh hôm nay")
    tong_ly = len(df)
    tong_loi = df["Lợi nhuận"].sum()
    best_seller = df["Món"].value_counts().idxmax()
    best_seller_so_ly = df["Món"].value_counts().max()

    st.markdown(f"- **Tổng số ly bán:** {tong_ly} ly")
    st.markdown(f"- **Tổng lợi nhuận:** {tong_loi}k")
    st.markdown(f"- **Món bán nhiều nhất:** {best_seller} ({best_seller_so_ly} ly)")

    # Biểu đồ cột
    st.markdown("### 📈 Biểu đồ số ly từng món")
    chart_data = df["Món"].value_counts().reset_index()
    chart_data.columns = ["Món", "Số ly"]
    fig, ax = plt.subplots()
    ax.barh(chart_data["Món"], chart_data["Số ly"], color="skyblue")
    ax.set_xlabel("Số ly")
    ax.set_ylabel("Món")
    ax.set_title("Số ly mỗi món đã bán hôm nay")
    st.pyplot(fig)
else:
    st.info("Chưa có đơn nào hôm nay.")
