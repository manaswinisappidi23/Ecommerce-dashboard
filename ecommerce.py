import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    page_icon="🛒",
    layout="wide"
)

# Title
st.title("🛒 E-Commerce Sales Analytics Dashboard")

# File Upload
uploaded_file = st.file_uploader(
    "Upload E-Commerce Dataset",
    type=["csv"]
)

if uploaded_file is not None:

    # Load Data
    df = pd.read_csv(uploaded_file)

    st.sidebar.header("Filters")

    # Convert Date Column
    if 'Order Date' in df.columns:
        df['Order Date'] = pd.to_datetime(df['Order Date'])

    # Sidebar Filters
    if 'Category' in df.columns:
        category = st.sidebar.multiselect(
            "Select Category",
            options=df['Category'].unique(),
            default=df['Category'].unique()
        )

        df = df[df['Category'].isin(category)]

    # KPIs
    total_sales = df['Sales'].sum()
    total_profit = df['Profit'].sum()
    total_orders = len(df)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Sales", f"${total_sales:,.2f}")
    col2.metric("Total Profit", f"${total_profit:,.2f}")
    col3.metric("Total Orders", total_orders)

    st.markdown("---")

    # Sales by Category
    if 'Category' in df.columns:
        sales_category = (
            df.groupby('Category')['Sales']
            .sum()
            .reset_index()
        )

        fig1 = px.bar(
            sales_category,
            x='Category',
            y='Sales',
            title='Sales by Category',
            text_auto=True
        )

        st.plotly_chart(fig1, use_container_width=True)

    # Monthly Sales Trend
    if 'Order Date' in df.columns:

        monthly_sales = (
            df.groupby(df['Order Date'].dt.to_period('M'))['Sales']
            .sum()
            .reset_index()
        )

        monthly_sales['Order Date'] = monthly_sales[
            'Order Date'
        ].astype(str)

        fig2 = px.line(
            monthly_sales,
            x='Order Date',
            y='Sales',
            markers=True,
            title='Monthly Sales Trend'
        )

        st.plotly_chart(fig2, use_container_width=True)

    # Top Products
    if 'Product Name' in df.columns:

        top_products = (
            df.groupby('Product Name')['Sales']
            .sum()
            .sort_values(ascending=False)
            .head(10)
            .reset_index()
        )

        fig3 = px.bar(
            top_products,
            x='Sales',
            y='Product Name',
            orientation='h',
            title='Top 10 Products'
        )

        st.plotly_chart(fig3, use_container_width=True)

    # Regional Sales
    if 'Region' in df.columns:

        region_sales = (
            df.groupby('Region')['Sales']
            .sum()
            .reset_index()
        )

        fig4 = px.pie(
            region_sales,
            names='Region',
            values='Sales',
            title='Regional Sales Distribution'
        )

        st.plotly_chart(fig4, use_container_width=True)

    # Raw Data
    with st.expander("View Dataset"):
        st.dataframe(df)

    # Download Filtered Data
    csv = df.to_csv(index=False)

    st.download_button(
        label="Download Filtered Data",
        data=csv,
        file_name="filtered_data.csv",
        mime="text/csv"
    )

else:
    st.info("Please upload an E-Commerce CSV file.")