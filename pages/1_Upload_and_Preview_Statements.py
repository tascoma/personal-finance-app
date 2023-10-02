import streamlit as st
import pandas as pd
import os


st.title("Upload and Preview Statements")

file = st.file_uploader("Upload Bank Statement, Credit Card, or Paystub")

if file:
    # Create the "uploads" folder if it doesn't exist
    os.makedirs("uploads", exist_ok=True)

    # Save the uploaded file to the "uploads" folder
    file_path = os.path.join("uploads", file.name)
    with open(file_path, "wb") as f:
        f.write(file.read())
    st.success("File uploaded successfully!")

# Display a preview of all files in the "uploads" folder
uploaded_files = os.listdir("uploads")

if uploaded_files:
    st.subheader("Uploaded Files")
    selected_file = st.selectbox("Select a file", uploaded_files)

    # Get the file extension
    file_extension = os.path.splitext(selected_file)[-1]

    # Preview the selected file based on the file extension
    if file_extension == ".csv":
        df = pd.read_csv(os.path.join("uploads", selected_file))
        st.subheader("Preview of the CSV file")
        st.dataframe(df)
    elif file_extension == ".xlsx":
        df = pd.read_excel(os.path.join("uploads", selected_file))
        st.subheader("Preview of the Excel file")
        st.dataframe(df)
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