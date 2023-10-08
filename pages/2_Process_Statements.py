import streamlit as st
import pandas as pd
import statement_processor
import sqlite3
import os
import shutil

st.title("Process Statements")

os.makedirs("processed", exist_ok=True)
uploaded_files = os.listdir("uploads")
processed_files = os.listdir("processed")
dfs = []

connection = sqlite3.connect('personal-finance.db')

# Display the files in "uploads" and "processed"
st.subheader("Uploaded Files")
if uploaded_files:
    for file in uploaded_files:
        st.write(file)
else:
    st.write("No files in uploads folder")

if st.button("Process Statements"):
    os.makedirs("processed", exist_ok=True)
    for file in uploaded_files:
        file_extension = os.path.splitext(file)[-1]
        if (file_extension == ".csv" or file_extension == '.xlsx') and 'creditcard' in file.lower():
            df = pd.read_csv(os.path.join('uploads', file))
            processed_df = statement_processor.process_creditcard_statements(df, connection)
       
        elif (file_extension == ".csv" or file_extension == '.xlsx') and 'bank' in file.lower():
            df = pd.read_csv(os.path.join('uploads', file))
            processed_df = statement_processor.process_bank_statements(df)

        elif file_extension == ".pdf":
            pdf = os.path.join('uploads', file)
            processed_df = statement_processor.process_paystub(pdf, connection)
        
        else:
            continue
        
        dfs.append(processed_df)
        upload_file_path = os.path.join("uploads", file)
        processed_file_path = os.path.join("processed", file)
        shutil.move(upload_file_path, processed_file_path)
    
    journal_entries_df = pd.concat(dfs).reset_index(drop=True)
    journal_entries_df['transaction_date'] = journal_entries_df['transaction_date'].dt.date
    journal_entries_df = journal_entries_df.sort_values(by=['transaction_date', 'transaction_id'], ascending=True).reset_index(drop=True)

    st.subheader("Preview of the Journal Entries")
    st.dataframe(journal_entries_df)

    missing_gl_code_df = statement_processor.missing_gl_code(journal_entries_df)
    st.subheader("Journal Entries missing GL Codes")
    st.dataframe(missing_gl_code_df)

    # df.to_sql("general_ledger", connection, if_exists="append", index=False)
    connection.close()

# Display the processed file names
st.subheader("Processed Files")
if processed_files:
    for file in processed_files:
        st.write(file)
else:
    st.write("No files have been processed yet")