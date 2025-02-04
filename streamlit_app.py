import streamlit as st
import pandas as pd
import os

@st.cache_data
def load_data(csv_path):
    if not os.path.exists(csv_path):
        st.error(f"CSV file not found: {csv_path}")
        return pd.DataFrame()
    return pd.read_csv(csv_path)

def main():
    st.title("Total Spend 2023/24")

    csv_path = "cleaned_totalSpend_23_24.csv"
    df = load_data(csv_path)
    
    # Display the dataframe (using st.dataframe for interactivity)
    if not df.empty:
        st.dataframe(df)
    else:
        st.write("No data available.")

if __name__ == "__main__":
    main()
