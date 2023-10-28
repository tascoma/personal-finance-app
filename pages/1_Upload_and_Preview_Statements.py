import streamlit as st
import pandas as pd
import os

# Set up the page settings
st.set_page_config(page_title="Upload and Preview Statements", layout="wide")
st.title("Upload and Preview Statements")

file = st.file_uploader("Upload Bank Statement, Credit Card, or Paystub")

if file:
    os.makedirs("uploads", exist_ok=True)
    file_path = os.path.join("uploads", file.name)
    with open(file_path, "wb") as f:
        f.write(file.read())
    st.success("File uploaded successfully!")

uploaded_files = os.listdir("uploads")

if uploaded_files:
    st.subheader("Uploaded Files")
    selected_file = st.selectbox("Select a file", uploaded_files)
    file_extension = os.path.splitext(selected_file)[-1]
    if file_extension == ".csv":
        df = pd.read_csv(os.path.join("uploads", selected_file))
        st.subheader("Preview of the CSV file")
        st.dataframe(df, width=2500)
    elif file_extension == ".xlsx":
        df = pd.read_excel(os.path.join("uploads", selected_file))
        st.subheader("Preview of the Excel file")
        st.dataframe(df, width=2500)
    elif file_extension == ".pdf":
        st.subheader("Preview Unavailable")
    else:
        st.subheader("Preview Unavailable")

    if st.button("Remove File"):
        file_to_remove = os.path.join("uploads", selected_file)
        os.remove(file_to_remove)
        st.success(f"{selected_file} has been removed.")

else:
    st.header("Add Files to Preview")