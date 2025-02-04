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

def paginate_dataframe(df, page_size, page_num):
    """Return one page of the dataframe"""
    total_pages = len(df) // page_size + (1 if len(df) % page_size > 0 else 0)
    start_idx = page_size * (page_num - 1)
    end_idx = min(start_idx + page_size, len(df))
    return df.iloc[start_idx:end_idx], total_pages

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
        
        with st.spinner("Loading MP Expenses data..."):
            df = load_data(mp_csv_path)
        
        if df.empty:
            st.write("No data available.")
        else:
            # Add pagination controls
            page_size = 1000  # Number of rows per page
            total_rows = len(df)
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col1:
                st.write(f"Total rows: {total_rows:,}")
            
            with col2:
                page_num = st.number_input("Page", min_value=1, 
                                         max_value=(total_rows // page_size) + 1,
                                         value=1)
            
            # Get the paginated data
            df_page, total_pages = paginate_dataframe(df, page_size, page_num)
            with col3:
                st.write(f"Page {page_num} of {total_pages}")
            
            # Display the paginated data without styling
            st.dataframe(
                df_page,
                use_container_width=True,
                hide_index=True
            )
    
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
                    # Add pagination for this view as well
                    page_size = 1000
                    total_rows = len(df)
                    
                    col1, col2, col3 = st.columns([1, 2, 1])
                    with col1:
                        st.write(f"Total rows: {total_rows:,}")
                    
                    with col2:
                        page_num = st.number_input("Page", min_value=1,
                                                 max_value=(total_rows // page_size) + 1,
                                                 value=1,
                                                 key="year_view_page")
                    
                    # Get the paginated data
                    df_page, total_pages = paginate_dataframe(df, page_size, page_num)
                    with col3:
                        st.write(f"Page {page_num} of {total_pages}")
                    
                    # Display the paginated data without styling
                    st.dataframe(
                        df_page,
                        use_container_width=True,
                        hide_index=True
                    )

if __name__ == "__main__":
    main()
