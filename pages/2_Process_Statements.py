import streamlit as st
import pandas as pd
import data_processor
import os

st.title("Process Statements")

uploaded_files = os.listdir("uploads")
processed_files = os.listdir("processed")

# Display the files in "uploads" and "processed"
st.subheader("Uploaded Files")
if uploaded_files:
    for file in uploaded_files:
        st.write(file)
else:
    st.write("No files in uploads folder")

st.subheader("Processed Files")
if processed_files:
    for file in processed_files:
        st.write(file)
else:
    st.write("No files in processed folder")

# Create the "processed" folder if it doesn't exist
os.makedirs("processed", exist_ok=True)

# Display a preview of all files in the "uploads" folder
uploaded_files = os.listdir("uploads")

if uploaded_files:
    st.subheader("Uploaded Files")
    selected_files = st.multiselect("Select files to process", uploaded_files)

    if st.button("Process Bank Statement(s)"):
        df = data_processor.process_bank_statements(selected_files)
        st.dataframe(df)
        data_processor.move_files_to_processed(selected_files=selected_files)
        
    if st.button("Process Credit Card Statement(s)"):
        df = data_processor.process_creditcard_statements(selected_files)
        st.dataframe(df)
        data_processor.move_files_to_processed(selected_files=selected_files)

    if st.button("Process Paystub(s)"):
        df = data_processor.process_paystubs(selected_files)
        st.dataframe(df)
        data_processor.move_files_to_processed(selected_files=selected_files)

else:
    st.subheader("Please upload files to process")