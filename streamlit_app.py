import streamlit as st
import pandas as pd
import os

# Set the app to use the full screen width
st.set_page_config(layout="wide")

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
    
    if df.empty:
        st.write("No data available.")
    else:
        # Apply custom styling via Pandas' Styler
        # This example aligns text to the left and adds padding to cells,
        # and also styles the header background and text color.
        styler = df.style.set_properties(**{
            'text-align': 'left',
            'white-space': 'nowrap'
        }).set_table_styles(
            [
                {'selector': 'th', 'props': [
                    ('background-color', '#f5f5f5'),
                    ('color', '#333'),
                    ('text-align', 'left'),
                    ('padding', '8px')
                ]},
                {'selector': 'td', 'props': [
                    ('padding', '8px')
                ]}
            ]
        )
        
        # Display the DataFrame using st.dataframe in full container width
        st.dataframe(styler, use_container_width=True)

if __name__ == "__main__":
    main()
