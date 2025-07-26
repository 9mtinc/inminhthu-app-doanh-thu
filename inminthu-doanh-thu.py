import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# --- Giá nguyên liệu (theo user cung cấp) ---
GIA_CA_PHE = 140_000 / 3000  # 140k cho 3kg → 1g = ?
GIA_DUONG = 12_000 / 500    # 12k cho 0.5kg → 1g = ?
GIA_TAC = 30_000 / 1000     # 30k cho 1kg → 1g = ?

# --- Công thức ước lượng chi phí nguyên liệu từng loại ---
CONG_THUC = {
    "Cà phê đen": {"cafe": 18, "duong": 10},
    "Cà phê sữa": {"cafe": 18, "duong": 20},
    "Cà phê muối": {"cafe": 18, "duong": 25},
    "Bạc xỉu": {"cafe": 10, "duong": 25},
    "Trà tắc": {"tac": 50, "duong": 15},
    "Trà đường": {"duong": 15},
    "Matcha muối": {"duong": 25},
}

GIA_BAN = {
    "Cà phê đen": {"M": 12, "L": 17, "XL": 20},
    "Cà phê sữa": {"M": 15, "L": 19, "XL": 23},
    "Cà phê muối": {"M": 16, "L": 21, "XL": 26},
    "Bạc xỉu": {"M": 17, "L": 22, "XL": 27},
    "Trà tắc": {"M": 8, "L": 10, "XL": 15},
    "Trà đường": {"M": 6, "L": 9, "XL": 10},
    "Matcha muối": {"M": 17, "L": 22, "XL": 26},
}

st.set_page_config(page_title="Quản lý bán cà phê", layout="wide")
st.title("☕ Quản lý bán hàng - INMINHTHU CAFÉ")

# --- Nhập dữ liệu ---
st.sidebar.header("➕ Nhập dữ liệu")
ngay = st.sidebar.date_input("Chọn ngày bán", format="DD/MM/YYYY")
thoi_gian = st.sidebar.time_input("Giờ bán (từng phút)", step=60)
khach_hang = st.sidebar.text_input("Tên khách hàng")
loai = st.sidebar.selectbox("Chọn loại thức uống", list(GIA_BAN.keys()))
kich_co = st.sidebar.radio("Size", ["M", "L", "XL"], horizontal=True)
them = st.sidebar.button("✅ Thêm vào danh sách")

if "data" not in st.session_state:
    st.session_state.data = []

if them:
    timestamp = datetime.combine(ngay, thoi_gian)
    st.session_state.data.append({
        "Thời gian": timestamp,
        "Khách hàng": khach_hang,
        "Loại": loai,
        "Size": kich_co
    })

# --- Xử lý chi phí nguyên liệu ---
def tinh_chi_phi(loai):
    cong_thuc = CONG_THUC.get(loai, {})
    chi_phi = 0
    chi_phi += cong_thuc.get("cafe", 0) * GIA_CA_PHE
    chi_phi += cong_thuc.get("duong", 0) * GIA_DUONG
    chi_phi += cong_thuc.get("tac", 0) * GIA_TAC
    return round(chi_phi, 1)

# --- Tính toán và hiển thị ---
data = pd.DataFrame(st.session_state.data)
if not data.empty:
    data["Doanh thu"] = data.apply(lambda row: GIA_BAN[row["Loại"]][row["Size"]], axis=1)
    data["Chi phí"] = data["Loại"].apply(tinh_chi_phi)
    data["Lợi nhuận"] = data["Doanh thu"] - data["Chi phí"]
    data["Ngày"] = data["Thời gian"].dt.strftime("%A, %d/%m/%Y")
    data["Giờ"] = data["Thời gian"].dt.strftime("%H:%M")

    st.subheader("📋 Dữ liệu bán hàng")
    st.dataframe(data[["Ngày", "Giờ", "Khách hàng", "Loại", "Size", "Doanh thu", "Chi phí", "Lợi nhuận"]], use_container_width=True)

    # --- Tổng kết theo ngày ---
    tong_ket = data.groupby("Ngày").agg({
        "Doanh thu": "sum",
        "Chi phí": "sum",
        "Lợi nhuận": "sum",
        "Loại": "count"
    }).rename(columns={"Loại": "Số ly bán"})

    mon_chay = data.groupby(["Ngày", "Loại"]).size().reset_index(name="Số lượng")
    mon_ban_chay = mon_chay.sort_values("Số lượng", ascending=False).drop_duplicates("Ngày")
    tong_ket = tong_ket.merge(mon_ban_chay[["Ngày", "Loại"]], on="Ngày", how="left").rename(columns={"Loại": "Bán chạy nhất"})

    st.subheader("📊 Thống kê tổng hợp")
    st.dataframe(tong_ket, use_container_width=True)

    # --- Biểu đồ doanh thu ---
    st.subheader("📈 Biểu đồ doanh thu và lợi nhuận theo ngày")
    fig, ax = plt.subplots()
    tong_ket[["Doanh thu", "Lợi nhuận"]].plot(kind="bar", ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

else:
    st.info("📌 Hãy thêm dữ liệu bán hàng từ thanh bên trái.")
