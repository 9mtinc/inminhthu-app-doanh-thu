import streamlit as st
import pandas as pd
from datetime import datetime, date, time
import plotly.express as px

st.set_page_config(page_title="INMINHTHU CAFÉ Bán Hàng", layout="wide")
st.title("☕ INMINHTHU CAFÉ - Quản lý bán hàng")

# File CSV lưu dữ liệu
DATA_FILE = "data.csv"

# Load dữ liệu nếu đã có
@st.cache_data
def load_data():
    try:
        df = pd.read_csv(DATA_FILE, parse_dates=['Thời gian'])
        return df
    except:
        return pd.DataFrame(columns=["Tên khách", "Món", "Size", "Số lượng", "Thời gian"])

# Lưu dữ liệu
def save_data(df):
    df.to_csv(DATA_FILE, index=False)

# ====== GIAO DIỆN NHẬP LIỆU ======
st.sidebar.header("📥 Nhập đơn hàng")
ten_khach = st.sidebar.text_input("Tên khách hàng")
mon = st.sidebar.selectbox("Chọn món", [
    "Cà phê đen", "Cà phê sữa", "Cà phê muối", "Bạc xỉu",
    "Trà tắc", "Trà đường", "Matcha latte", "Matcha macchiato"
])
size = st.sidebar.selectbox("Chọn size", ["M", "L", "XL"])
so_luong = st.sidebar.number_input("Số lượng", min_value=1, value=1)

# Ngày và giờ bán (người dùng chọn thủ công)
ngay_ban = st.sidebar.date_input("📅 Chọn ngày bán", value=date.today())
gio_ban = st.sidebar.time_input("⏰ Chọn giờ bán (giờ:phút)", value=datetime.now().time())
thoi_gian = datetime.combine(ngay_ban, gio_ban)

if st.sidebar.button("✅ Lưu đơn"):
    new_data = pd.DataFrame({
        "Tên khách": [ten_khach],
        "Món": [mon],
        "Size": [size],
        "Số lượng": [so_luong],
        "Thời gian": [thoi_gian]
    })
    df = pd.concat([load_data(), new_data], ignore_index=True)
    save_data(df)
    st.sidebar.success("Đã lưu đơn hàng!")

# ====== GIAO DIỆN XEM DỮ LIỆU ======
st.header("📊 Thống kê theo ngày")

# Chọn ngày cần xem
df = load_data()
df["Ngày"] = df["Thời gian"].dt.date
df["Giờ"] = df["Thời gian"].dt.strftime("%H:%M")
df["Thứ"] = df["Thời gian"].dt.strftime("%A")

if df.empty:
    st.info("Chưa có dữ liệu.")
else:
    ngay_xem = st.date_input("📆 Chọn ngày để xem thống kê", value=date.today())
    df_ngay = df[df["Ngày"] == ngay_xem]

    if df_ngay.empty:
        st.warning("Không có đơn nào trong ngày này.")
    else:
        # Hiển thị danh sách đơn hàng
        st.subheader(f"📝 Danh sách khách ngày {df_ngay['Thứ'].iloc[0]}, {ngay_xem.strftime('%d/%m/%Y')}")
        st.dataframe(df_ngay[["Tên khách", "Món", "Size", "Số lượng", "Giờ"]], use_container_width=True)

        # Tổng số ly
        tong_ly = df_ngay["Số lượng"].sum()
        st.metric("🥤 Tổng số ly bán", tong_ly)

        # Món bán chạy nhất
        top_mon = df_ngay.groupby("Món")["Số lượng"].sum().sort_values(ascending=False)
        mon_top = top_mon.idxmax()
        st.metric("🔥 Món bán chạy nhất", f"{mon_top} ({top_mon.max()} ly)")

        # Biểu đồ cột số lượng theo món
        chart1 = px.bar(top_mon, x=top_mon.index, y=top_mon.values, labels={"x": "Món", "y": "Số lượng"},
                        title="Biểu đồ số lượng theo món", color=top_mon.index)
        st.plotly_chart(chart1, use_container_width=True)

        # Biểu đồ tròn
        chart2 = px.pie(df_ngay, names="Món", values="Số lượng", title="Tỷ lệ các món bán ra")
        st.plotly_chart(chart2, use_container_width=True)

        # Nếu nhiều ngày có dữ liệu, thêm line chart theo thời gian
        if df["Ngày"].nunique() > 1:
            trend = df.groupby("Ngày")["Số lượng"].sum()
            chart3 = px.line(trend, x=trend.index, y=trend.values, labels={"x": "Ngày", "y": "Tổng số ly"},
                             title="📈 Xu hướng bán theo ngày")
            st.plotly_chart(chart3, use_container_width=True)
