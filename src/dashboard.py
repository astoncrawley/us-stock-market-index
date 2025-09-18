# Streamlit dashboard for stock analysis

# Import libraries
import os
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st


# Select stock symbols
stock_tickers = [
    "AAPL",  # Apple Inc.
    "AMZN",  # Amazon.com Inc.
    "GOOGL", # Alphabet Inc. (Google)
    "MSFT"   # Microsoft Corporation
]

# Load and concatinate data from multiple CSV files into a single DataFrame
df = pd.DataFrame()

for ticker in stock_tickers:
    file_path = os.path.join("..", "data", f"{ticker}_data.csv")
    # file_path = os.path.join("data", f"{ticker}_data.csv")
    print(os.getcwd())
    print(file_path)
    temp_df = pd.read_csv(file_path)
    
    df = pd.concat([df, temp_df], ignore_index=True)

# Convert "date" column to datetime format
df["date"] = pd.to_datetime(df["date"])

# Confirm unique stock names
stock_names = df["Name"].unique()






# Streamlit dashboard configuration
st.set_page_config(
    page_title="US Stock Analysis Dashboard",
    page_icon="📊",
    layout="wide"
)
st.title("Tech Stock Analysis Dashboard")

st.sidebar.title("Choose a Company")

selected_company = st.sidebar.selectbox(
    "Select a stock",
    stock_names
)

company_df = df[df["Name"] == selected_company]
company_df.sort_values(by="date", inplace=True)



# 1st plot
st.subheader(f"1. Closing Price of {selected_company} Over Time")
fig1 = px.line(
    company_df,
    x="date",
    y="close",
    title=f"{selected_company} Closing Price Over Time",
    labels={"date": "Date", "close": "Closing Price (USD)"},
    template="plotly_dark"
)
st.plotly_chart(fig1, use_container_width=True)


# 2nd plot
st.subheader(f"2. Moving Averages (10, 20, 50 days) of {selected_company}")

# Create a moving average dataframe and add 10, 20 and 50 day moving average windows for each stock
moving_avg_windows = [10, 20, 50]

for window in moving_avg_windows:
    company_df[f"close_{window}"] = company_df["close"].rolling(window).mean()

fig2 = px.line(
    company_df,
    x="date",
    y=["close", "close_10", "close_20", "close_50"],
    title=f"{selected_company} Closing Price Over Time with Moving Averages",
    labels={"date": "Date", "close": "Closing Price (USD)"},
    template="plotly_dark"
)
st.plotly_chart(fig2, use_container_width=True)


# 3rd plot
st.subheader(f"3. Daily Returns of {selected_company}")

# Add a new column calculating daily percentage change in closing prices
company_df["change"] = company_df["close"].pct_change() * 100

fig3 = px.line(
    company_df,
    x="date",
    y="change",
    title=f"Daily Returns of {selected_company} (%)",
    labels={"date": "Date", "change": "Daily Return (%)"},
    template="plotly_dark"
)
st.plotly_chart(fig3, use_container_width=True)


# 4th plot
st.subheader(f"4. Resampled Closing Price (Monthly, Quarterly, Yearly) of {selected_company} Over Time")

company_df.set_index("date", inplace=True)
resample_option = st.radio(
    "Select Resampling Frequency",
    ("Monthly", "Quarterly", "Yearly")
    # key="resample_freq"
)

if resample_option == "Monthly":
    resampled_df = company_df["close"].resample("M").mean()
elif resample_option == "Quarterly":
    resampled_df = company_df["close"].resample("Q").mean()
elif resample_option == "Yearly":
    resampled_df = company_df["close"].resample("Y").mean()
else:
    resampled_df = company_df["close"].resample("A").mean()

fig4 = px.line(
    resampled_df,
    # x="date",
    # y="change",
    title=f"{selected_company} {resample_option} Average Closing Price Over Time",
    # labels={"date": "Date", "chage": "Daily Return (%)"},
    template="plotly_dark"
)
st.plotly_chart(fig4, use_container_width=True)


# 5th plot
st.subheader(f"5. Correlation Between Companies (Closing Price)")

# Create new dataframe with closing prices of all stocks
close_df = pd.DataFrame()

for stock in stock_tickers:
    stock_data = df[df["Name"] == stock][["date", "close"]].copy()
    stock_data.set_index("date", inplace=True)
    close_df[stock] = stock_data["close"]

# Produce a heatmap to visualise the correlation matrix
fig5 , ax = plt.subplots()
sns.heatmap(close_df.corr(), annot=True, cmap="coolwarm", ax=ax)
st.pyplot(fig5, use_container_width=True)

st.markdown("---")
st.markdown("***Note:*** Data is sourced from Yahoo Finance and may not be up-to-date or accurate. Please verify with official sources before making any investment decisions.")
st.markdown("Developed by Aston Crawley")
st.markdown("2025 © All rights reserved.")