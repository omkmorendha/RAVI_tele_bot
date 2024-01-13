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
    s3_parts = url.split("/")
    bucket_name_extra = s3_parts[2]
    bucket_name = re.match(r'^([^\.]+)\.', bucket_name_extra).group(1)
    object_key = "/".join(s3_parts[3:])

    try:
        # Create a Boto3 S3 client
        s3_client = boto3.client(
            "s3",
            region_name='eu-north-1',
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            config=boto3.session.Config(signature_version='s3v4')
        )

        # Get a pre-signed URL for the S3 object
        presigned_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': object_key},
            ExpiresIn=3600  # URL expiration time in seconds (adjust as needed)
        )

        # Create a custom HTML button with JavaScript to trigger the file download
        download_button = f'<a href="{presigned_url}" download>Download {object_key}</a>'
        st.markdown(download_button, unsafe_allow_html=True)

    except Exception as e:
        st.error(f"An error occurred while generating the download link: {e}")

        
def table_ind_page():
    st.title("RAVI BOT SUBMISSIONS")

    query = "SELECT * FROM user_data" 
    df = pd.read_sql(query, engine)

    # Display the table using Streamlit with a button for each row
    for index, row in df.iterrows():
        # Button to open sidebar for the current row
        if st.button(f"Download Files for Individual {index + 1}"):
            # Sidebar content for the current row
            st.sidebar.title(f"Individual {index + 1} Details")

            # Display other columns if needed
            st.sidebar.write("Data:")
            st.sidebar.write(row.drop(["Final_Testimony_URL", "Additional_Evidence_URL"]))

            # Display Final Testimony Files
            st.sidebar.write("\nFinal Testimony Files:")
            final_testimony_urls = row["Final_Testimony_URL"]
            if final_testimony_urls:
                final_testimony_urls = final_testimony_urls.split()
                for url in final_testimony_urls:
                    download_s3_object(url)
                    st.sidebar.write(f"- [View {os.path.basename(url)}]({url})")
            else:
                st.sidebar.write("No Files available")

            # Display Additional Evidence Files
            st.sidebar.write("\nAdditional Evidence Files:")
            additional_evidence_urls = row["Additional_Evidence_URL"]
            if additional_evidence_urls:
                additional_evidence_urls = additional_evidence_urls.split()
                for url in additional_evidence_urls:
                    download_s3_object(url)
                    st.sidebar.write(f"- [View {os.path.basename(url)}]({url})")
            else:
                st.sidebar.write("No Files available")


def table_full_page():
    st.title("RAVI BOT SUBMISSIONS")

    query = "SELECT * FROM user_data" 
    df = pd.read_sql(query, engine)

    # Display the table using Streamlita
    df.index += 1
    st.dataframe(df, width=0, height=0)

def main():
    st.set_page_config(layout="wide")

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
                "View and Download Individual Testimonies and Evidence",
                "Reset Password"
            ),
        )
        
        if data == "View and Download Individual Testimonies and Evidence":
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