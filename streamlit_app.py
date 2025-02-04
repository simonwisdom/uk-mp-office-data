import streamlit as st
import pandas as pd
import os
import dask.dataframe as dd

# Set the app to use the full screen width
st.set_page_config(layout="wide")

@st.cache_data
def load_data(csv_path):
    if not os.path.exists(csv_path):
        st.error(f"CSV file not found: {csv_path}")
        return pd.DataFrame()
    return pd.read_csv(csv_path)

@st.cache_data
def load_mp_expenses(csv_path):
    if not os.path.exists(csv_path):
        st.error(f"CSV file not found: {csv_path}")
        return None
    # Load the large CSV using Dask
    return dd.read_csv(csv_path)

def main():
    st.title("MP Spending Dashboard")
    
    # Add a sidebar to select the view
    view_option = st.sidebar.selectbox("Select dataset view", (
        "Total Spend 2023/24", 
        "MP Expenses", 
        "MP Office Expense Claims by Year"
    ))
    
    if view_option == "Total Spend 2023/24":
        st.header("Total Spend 2023/24")
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
    
    elif view_option == "MP Expenses":
        st.header("MP Software Expenses, 2023-2024")
        mp_csv_path = "Top MP Office Claims for Software & Applications, 2024.csv"
        df_dask = load_mp_expenses(mp_csv_path)
        
        if df_dask is None:
            st.write("No data available.")
        else:
            # Provide a slider to choose how many rows to preview from the large dataset
            rows_to_display = st.slider("Number of rows to preview", 10, 1000, 100)
            
            with st.spinner("Loading MP Expenses data..."):
                # Load a preview of the data; note that dd.head() returns a pandas DataFrame
                df_preview = df_dask.head(rows_to_display)
            
            # Optionally, apply custom styling to the preview
            styler = df_preview.style.set_properties(**{
                'text-align': 'left',
                'white-space': 'nowrap'
            }).set_table_styles(
                [
                    {'selector': 'th', 'props': [
                        ('background-color', '#e0e0e0'),
                        ('color', '#000'),
                        ('text-align', 'left'),
                        ('padding', '8px')
                    ]},
                    {'selector': 'td', 'props': [
                        ('padding', '8px')
                    ]}
                ]
            )
            
            st.dataframe(styler, use_container_width=True)
            st.write(f"Previewing the first {rows_to_display} rows of the MP Expenses dataset. "
                     "The full dataset is large and is loaded with Dask for efficiency.")
    
    elif view_option == "MP Office Expense Claims by Year":
        st.header("MP Office Expense Claims by Year")
        folder_path = "mp_office_expense_claims"
        
        if not os.path.isdir(folder_path):
            st.error(f"Folder not found: {folder_path}")
        else:
            csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
            if not csv_files:
                st.write("No CSV files found in this folder.")
            else:
                selected_file = st.selectbox("Select a year file", sorted(csv_files))
                full_path = os.path.join(folder_path, selected_file)
                
                with st.spinner(f"Loading data from {selected_file}..."):
                    df = load_data(full_path)
                
                if df.empty:
                    st.write("No data available in the selected file.")
                else:
                    rows_to_display = st.slider("Number of rows to preview", 10, 1000, 100)
                    # Apply custom styling to the preview.
                    styler = df.head(rows_to_display).style.set_properties(**{
                        'text-align': 'left',
                        'white-space': 'nowrap'
                    }).set_table_styles(
                        [
                            {'selector': 'th', 'props': [
                                ('background-color', '#d0e0f0'),
                                ('color', '#000'),
                                ('text-align', 'left'),
                                ('padding', '8px')
                            ]},
                            {'selector': 'td', 'props': [
                                ('padding', '8px')
                            ]}
                        ]
                    )
                    
                    st.dataframe(styler, use_container_width=True)
                    st.write(f"Previewing the first {rows_to_display} rows from {selected_file}.")

if __name__ == "__main__":
    main()
