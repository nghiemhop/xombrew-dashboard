import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title='Dashboard Xom Brew', layout='wide')
st.title('☕ Dashboard doanh thu Xom Brew')

@st.cache_data(ttl=3600)   # tự đọc lại dữ liệu sau mỗi 1 giờ
def load():
    return pd.read_csv('du_lieu_sach.csv', parse_dates=['Ngày'])

df = load()

# ---- Bộ lọc ----
st.sidebar.header('Bộ lọc')
if st.sidebar.button('🔄 Làm mới dữ liệu'):
    st.cache_data.clear()
    st.rerun()

thang = st.sidebar.multiselect('Tháng', sorted(df['Tháng'].unique()), default=sorted(df['Tháng'].unique()))
ch    = st.sidebar.multiselect('Cửa hàng', sorted(df['Cửa hàng'].unique()), default=sorted(df['Cửa hàng'].unique()))
nhom  = st.sidebar.multiselect('Nhóm sản phẩm', sorted(df['Nhóm SP'].unique()), default=sorted(df['Nhóm SP'].unique()))

d = df[df['Tháng'].isin(thang) & df['Cửa hàng'].isin(ch) & df['Nhóm SP'].isin(nhom)]

# ---- Chỉ số ----
c1, c2, c3 = st.columns(3)
c1.metric('Tổng doanh thu', f"{d['Thành tiền'].sum():,.0f} USD")
c2.metric('Số giao dịch', f"{d['Mã GD'].nunique():,}")
c3.metric('Số sản phẩm đã bán', f"{d['SL'].sum():,}")

# ---- Đồ thị ----
col1, col2 = st.columns(2)
nhom_df = d.groupby('Nhóm SP', as_index=False)['Thành tiền'].sum().sort_values('Thành tiền')
col1.plotly_chart(px.bar(nhom_df, x='Thành tiền', y='Nhóm SP', orientation='h',
                         title='Doanh thu theo nhóm sản phẩm'), width='stretch')

thang_df = d.groupby('Tháng', as_index=False)['Thành tiền'].sum()
col2.plotly_chart(px.line(thang_df, x='Tháng', y='Thành tiền', markers=True,
                          title='Doanh thu theo tháng'), width='stretch')

col3, col4 = st.columns(2)
ch_df = d.groupby('Cửa hàng', as_index=False)['Thành tiền'].sum()
col3.plotly_chart(px.pie(ch_df, names='Cửa hàng', values='Thành tiền',
                         title='Tỷ trọng doanh thu theo cửa hàng'), width='stretch')

gio_df = d.groupby('Giờ bán', as_index=False)['Thành tiền'].sum()
col4.plotly_chart(px.bar(gio_df, x='Giờ bán', y='Thành tiền',
                         title='Doanh thu theo giờ'), width='stretch')

top = d.groupby('Tên SP', as_index=False)['Thành tiền'].sum().nlargest(10, 'Thành tiền')
st.plotly_chart(px.bar(top.sort_values('Thành tiền'), x='Thành tiền', y='Tên SP',
                       orientation='h', title='Top 10 sản phẩm'), width='stretch')
