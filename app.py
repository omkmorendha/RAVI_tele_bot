import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import os

AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
RDS_HOST = os.environ.get("RDS_HOST")
RDS_USER = os.environ.get("RDS_USER")
RDS_PASSWORD = os.environ.get("RDS_PASSWORD")
RDS_PORT = int(os.environ.get("RDS_PORT"))
RDS_DATABASE = os.environ.get("RDS_DATABASE")
S3_BUCKET_NAME = os.environ.get("S3_BUCKET_NAME")

# Create a connection to the RDS database
engine = create_engine(f"mysql+mysqlconnector://{RDS_USER}:{RDS_PASSWORD}@{RDS_HOST}:{RDS_PORT}/{RDS_DATABASE}")


def main():
    st.title("Amazon RDS Table Viewer")

    query = "SELECT * FROM user_data" 
    df = pd.read_sql(query, engine)

    # Display the table using Streamlit
    st.write("### Table from Amazon RDS")
    st.dataframe(df)

if __name__ == "__main__":
    main()
