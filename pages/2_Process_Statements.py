import streamlit as st
import pandas as pd
from pandas import DataFrame
import statement_processor
import sqlite3
import os
import shutil

# Define a function to process uploaded statements
@st.cache_data
def process_statements(uploaded_files:list, _connection) -> DataFrame:
    """
    Process uploaded statements and return a DataFrame of journal entries.

    Args:
    uploaded_files (list): A list of file names to process.
    _connection: A SQLite3 database connection object.

    Returns:
    DataFrame: A DataFrame of journal entries.
    """
    # Create a directory to store processed files
    os.makedirs("processed", exist_ok=True)
    dfs = []
    for file in uploaded_files:
        file_extension = os.path.splitext(file)[-1]
        # Process credit card statements
        if (file_extension == ".csv" or file_extension == '.xlsx') and 'creditcard' in file.lower():
            df = pd.read_csv(os.path.join('uploads', file))
            processed_df = statement_processor.process_creditcard_statements(df, _connection)
        # Process bank statements
        elif (file_extension == ".csv" or file_extension == '.xlsx') and 'bank' in file.lower():
            df = pd.read_csv(os.path.join('uploads', file))
            processed_df = statement_processor.process_bank_statements(df)
        # Process pay stubs
        elif file_extension == ".pdf":
            pdf = os.path.join('uploads', file)
            processed_df = statement_processor.process_paystub(pdf, _connection)
        # Skip files with unsupported extensions or names
        else:
            continue
        
        # Append the processed DataFrame to a list
        dfs.append(processed_df)
        # Move the uploaded file to the processed directory
        upload_file_path = os.path.join("uploads", file)
        processed_file_path = os.path.join("processed", file)
        shutil.move(upload_file_path, processed_file_path)
    
    # Concatenate all the DataFrames and sort by date and transaction ID
    journal_entries_df = pd.concat(dfs).reset_index(drop=True)
    journal_entries_df['transaction_date'] = pd.to_datetime(journal_entries_df['transaction_date'])
    journal_entries_df['transaction_date'] = journal_entries_df['transaction_date'].dt.date
    journal_entries_df = journal_entries_df.sort_values(by=['transaction_date', 'transaction_id'], ascending=True).reset_index(drop=True)
    return journal_entries_df


# Set up the Streamlit page
st.title("Process Statements")
os.makedirs("processed", exist_ok=True)
uploaded_files = os.listdir("uploads")
processed_files = os.listdir("processed")
st.write("Number of Files to Process:", len(uploaded_files))

# Process statements when the button is clicked
if st.button("Process Statements"):
    connection = sqlite3.connect('personal-finance.db')
    journal_entries_df = process_statements(uploaded_files, connection)
    missing_gl_code_df = statement_processor.missing_gl_code(journal_entries_df)
    st.subheader("Preview of the Journal Entries")
    st.dataframe(journal_entries_df, width=2500)
    st.subheader("Journal Entries missing GL Codes")
    st.dataframe(missing_gl_code_df, width=2500)
    journal_entries_df.to_sql('general_ledger', connection, if_exists='append', index=False)
    st.write("Number of Journal Entries added to the database:", len(journal_entries_df))
    st.write("Number of Files Processed:", len(processed_files))
    connection.commit()
    connection.close()