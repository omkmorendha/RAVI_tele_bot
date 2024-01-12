import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import yaml
import boto3
import re
from yaml.loader import SafeLoader

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

load_dotenv()

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

def save():
    with open('config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)
        
def download_s3_object(url):
    # Extract the bucket name and object key from the S3 URL
    # Example URL: https://your-bucket.s3.amazonaws.com/your-object-key
    s3_parts = url.split("/")
    bucket_name_extra = s3_parts[2]
    bucket_name = re.match(r'^([^\.]+)\.', bucket_name_extra).group(1)
    object_key = "/".join(s3_parts[3:])

    try:
        # Create a Boto3 S3 client
        s3_client = boto3.client(
            "s3",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY
        )

        response = s3_client.get_object(Bucket=bucket_name, Key=object_key)
        content = response["Body"].read()

        # Save the content to a local file
        local_filename = object_key.split("/")[-1]
        with open(local_filename, "wb") as local_file:
            local_file.write(content)
            
    except Exception as e:
        print(f"An error occurred while downloading the object: {e}")
        
def table_ind_page():
    st.title("Amazon RDS Table Viewer")

    query = "SELECT * FROM user_data"
    df = pd.read_sql(query, engine)

    # Display the table using Streamlit
    st.write("### Table from Amazon RDS")

    # Iterate through each row and make final_testimony_url and Additional_Evidence_URL clickable
    for index, row in df.iterrows():
        st.write(f"#### Row {index + 1}")

        # Make final_testimony_url clickable
        st.write("Final Testimony URL:")
        final_testimony_urls = row["Final_Testimony_URL"]
        if final_testimony_urls:
            final_testimony_urls = final_testimony_urls.split()
            for url in final_testimony_urls:
                st.write(f"[{url}]({url})")

                # Add a download button for each URL
                download_button_label = "Download"
                if st.button(download_button_label):
                    download_s3_object(url)
        else:
            st.write("No URLs available")

        # Make Additional_Evidence_URL clickable
        st.write("Additional Evidence URL:")
        additional_evidence_urls = row["Additional_Evidence_URL"]
        if additional_evidence_urls:
            additional_evidence_urls = additional_evidence_urls.split()
            for url in additional_evidence_urls:
                st.write(f"[{url}]({url})")

                # Add a download button for each URL
                download_button_label = "Download"
                if st.button(download_button_label):
                    download_s3_object(url)
        else:
            st.write("No URLs available")

        # Display other columns if needed
        st.write("Other Columns:")
        st.write(row.drop(["Final_Testimony_URL", "Additional_Evidence_URL"]))


def table_full_page():
    st.title("Amazon RDS Table Viewer")

    query = "SELECT * FROM user_data" 
    df = pd.read_sql(query, engine)

    # Display the table using Streamlit
    st.write("### Table from Amazon RDS")
    st.dataframe(df)

def main():
    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
    )
    name, authentication_status, username = authenticator.login('Login', 'main')
    
    if st.session_state["authentication_status"]:
        data = st.selectbox(
            "Option",
            (
                "See Full Database",
                "See Individuals",
                "Reset Password"
            ),
        )
        
        if data == "See Individuals":
            table_ind_page()
        
        if data == "See Full Database":
            table_full_page()
        
        elif data == "Reset Password":
            if authenticator.reset_password(username, 'Reset password'):
                st.success('Password modified successfully')
                save()
            
        authenticator.logout('Logout', 'main')
        
    elif st.session_state["authentication_status"] == False:
        st.error('Username/password is incorrect')
    elif st.session_state["authentication_status"] == None:
        st.warning('Please enter your username and password')
        
if __name__ == "__main__":
    main()