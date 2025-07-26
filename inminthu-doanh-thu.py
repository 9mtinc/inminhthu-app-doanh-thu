# Streamlit app code for calculating drink profits with input form and chart
import streamlit as st
import pandas as pd
import datetime

# Sample profit data (pre-calculated from earlier analysis)
data = [
    {"Drink": "Cà phê muối", "Size": "1l", "Price": 26000, "Cost": 6938.44, "Profit": 19061.56},
    {"Drink": "Bạc xỉu", "Size": "1l", "Price": 27000, "Cost": 9842.28, "Profit": 17157.72},
    {"Drink": "Cà phê sữa", "Size": "1l", "Price": 23000, "Cost": 6938.44, "Profit": 16061.56},
    {"Drink": "Cà phê muối", "Size": "800ml", "Price": 21000, "Cost": 5460.62, "Profit": 15539.38},
    {"Drink": "Matcha latte muối", "Size": "1l", "Price": 28000, "Cost": 12958.69, "Profit": 15041.31},
    {"Drink": "Cà phê đen", "Size": "1l", "Price": 20000, "Cost": 5261.00, "Profit": 14739.00},
    {"Drink": "Matcha latte muối", "Size": "800ml", "Price": 24000, "Cost": 9310.87, "Profit": 14689.13},
    {"Drink": "Bạc xỉu", "Size": "800ml", "Price": 22000, "Cost": 7404.21, "Profit": 14595.79},
    {"Drink": "Cà phê sữa", "Size": "800ml", "Price": 19000, "Cost": 5460.62, "Profit": 13539.38},
    {"Drink": "Matcha latte", "Size": "1l", "Price": 26000, "Cost": 12958.69, "Profit": 13041.31},
    {"Drink": "Matcha latte", "Size": "800ml", "Price": 22000, "Cost": 9310.87, "Profit": 12689.13},
    {"Drink": "Cà phê đen", "Size": "800ml", "Price": 17000, "Cost": 4409.33, "Profit": 12590.67},
    {"Drink": "Matcha latte muối", "Size": "500ml", "Price": 19000, "Cost": 6584.05, "Profit": 12415.95},
    {"Drink": "Bạc xỉu", "Size": "500ml", "Price": 17000, "Cost": 5177.13, "Profit": 11822.87},
    {"Drink": "Cà phê muối", "Size": "500ml", "Price": 16000, "Cost": 4427.13, "Profit": 11572.87},
    {"Drink": "Cà phê sữa", "Size": "500ml", "Price": 15000, "Cost": 4427.13, "Profit": 10572.87},
    {"Drink": "Matcha latte", "Size": "500ml", "Price": 17000, "Cost": 6584.05, "Profit": 10415.95},
    {"Drink": "Cà phê đen", "Size": "500ml", "Price": 12000, "Cost": 3535.33, "Profit": 8464.67},
]

df = pd.DataFrame(data)

# Streamlit UI
st.set_page_config(page_title="INMINHTHU Cafe", layout="wide")
st.markdown("""
    <style>
        body {background-color: black; color: white;}
        .main {color: white;}
    </style>
""", unsafe_allow_html=True)

st.title("INMINHTHU Cafe - Tính Doanh Thu & Lợi Nhuận")

# Input section
with st.form("sales_form"):
    col1, col2, col3 = st.columns(3)
    with col1:
        name = st.text_input("Tên khách hàng")
    with col2:
        date = st.date_input("Ngày bán", value=datetime.date.today())
    with col3:
        time = st.time_input("Giờ bán", value=datetime.datetime.now().time())

    drink = st.selectbox("Chọn loại nước", df['Drink'].unique())
    size = st.selectbox("Chọn size", df[df['Drink'] == drink]['Size'].unique())
    quantity = st.number_input("Số lượng", min_value=1, value=1)

    submitted = st.form_submit_button("Tính toán")

if submitted:
    item = df[(df['Drink'] == drink) & (df['Size'] == size)].iloc[0]
    total_price = item['Price'] * quantity
    total_cost = item['Cost'] * quantity
    total_profit = item['Profit'] * quantity

    st.subheader("Kết quả giao dịch")
    st.write(f"Khách hàng: {name}")
    st.write(f"Ngày bán: {date.strftime('%d/%m/%Y')} - Giờ: {time.strftime('%H:%M')}")
    st.write(f"Món: {drink} ({size}) x {quantity}")
    st.write(f"Doanh thu: {total_price:,.0f} đồng")
    st.write(f"Chi phí: {total_cost:,.0f} đồng")
    st.write(f"Lợi nhuận: {total_profit:,.0f} đồng")

# Chart section
st.subheader("Biểu đồ lợi nhuận tối đa theo món")
df_grouped = df.groupby("Drink")["Profit"].sum().sort_values(ascending=False)
st.bar_chart(df_grouped)

st.caption("Made by INMINHTHU")
