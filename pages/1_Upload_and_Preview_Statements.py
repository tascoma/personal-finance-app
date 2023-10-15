import streamlit as st
import pandas as pd
import os

# Set up the page title
st.title("Upload and Preview Statements")

# Allow the user to upload a file
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
    # If there are uploaded files, display them in a dropdown menu
    st.subheader("Uploaded Files")
    selected_file = st.selectbox("Select a file", uploaded_files)

    # Get the file extension
    file_extension = os.path.splitext(selected_file)[-1]

    # Preview the selected file based on the file extension
    if file_extension == ".csv":
        # If the file is a CSV, display a preview of the data
        df = pd.read_csv(os.path.join("uploads", selected_file))
        st.subheader("Preview of the CSV file")
        st.dataframe(df)
    elif file_extension == ".xlsx":
        # If the file is an Excel file, display a preview of the data
        df = pd.read_excel(os.path.join("uploads", selected_file))
        st.subheader("Preview of the Excel file")
        st.dataframe(df)
    elif file_extension == ".pdf":
        # If the file is a PDF, display a message that previews are unavailable
        st.subheader("Preview Unavailable")
    else:
        # If the file is not a CSV, Excel, or PDF, display a message that previews are unavailable
        st.subheader("Preview Unavailable")
    
    # Allow the user to remove the selected file
    if st.button("Remove File"):
        file_to_remove = os.path.join("uploads", selected_file)
        os.remove(file_to_remove)
        st.success(f"{selected_file} has been removed.")

else:
    # If there are no uploaded files, display a message prompting the user to add files
    st.header("Add Files to Preview")