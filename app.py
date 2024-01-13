import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import yaml
import boto3
import re
import base64
from io import BytesIO, StringIO
import zipfile
from yaml.loader import SafeLoader

with open("./config.yaml") as file:
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
engine = create_engine(
    f"mysql+mysqlconnector://{RDS_USER}:{RDS_PASSWORD}@{RDS_HOST}:{RDS_PORT}/{RDS_DATABASE}"
)


def save():
    with open("config.yaml", "w") as file:
        yaml.dump(config, file, default_flow_style=False)


def download_s3_objects_as_zip(urls, zip_filename):
    try:
        s3_client = boto3.client(
            "s3",
            region_name="eu-north-1",
            aws_access_key_id=AWS_ACCESS_KEY_ID,
            aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
            config=boto3.session.Config(signature_version="s3v4"),
        )

        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zip_file:
            for url in urls:
                s3_parts = url.split("/")
                bucket_name_extra = s3_parts[2]
                bucket_name = re.match(r"^([^\.]+)\.", bucket_name_extra).group(1)
                object_key = "/".join(s3_parts[3:])
                file_data = s3_client.get_object(Bucket=bucket_name, Key=object_key)[
                    "Body"
                ].read()
                zip_file.writestr(os.path.basename(object_key), file_data)

        zip_buffer.seek(0)

        st.markdown(
            f'<a href="data:application/zip;base64,{base64.b64encode(zip_buffer.getvalue()).decode()}" '
            f'download="{zip_filename}.zip">Download All Files as Zip</a>',
            unsafe_allow_html=True,
        )

    except Exception as e:
        st.error(f"An error occurred while generating the download link: {e}")


def table_ind_page():
    st.title("RAVI BOT SUBMISSIONS")

    query = "SELECT * FROM user_data"
    df = pd.read_sql(query, engine)

    for index, row in df.iterrows():
        if st.button(f"Download Files for Individual {index + 1}"):
            st.sidebar.title(f"Individual {index + 1} Details")
            st.sidebar.write("Data:")
            st.sidebar.write(
                row.drop(["Final_Testimony_URL", "Additional_Evidence_URL"])
            )

            final_testimony_urls = row["Final_Testimony_URL"]
            if final_testimony_urls:
                final_testimony_urls = final_testimony_urls.split()
                st.sidebar.write("\nFinal Testimony Files:")
                for url in final_testimony_urls:
                    st.sidebar.write(f"- [View {os.path.basename(url)}]({url})")

            additional_evidence_urls = row["Additional_Evidence_URL"]
            if additional_evidence_urls:
                additional_evidence_urls = additional_evidence_urls.split()
                st.sidebar.write("\nAdditional Evidence Files:")
                for url in additional_evidence_urls:
                    st.sidebar.write(f"- [View {os.path.basename(url)}]({url})")

            if additional_evidence_urls or final_testimony_urls:
                urls = []
                if isinstance(final_testimony_urls, list) and isinstance(
                    additional_evidence_urls, list
                ):
                    urls = additional_evidence_urls + final_testimony_urls
                elif isinstance(final_testimony_urls, list):
                    urls = final_testimony_urls
                elif isinstance(additional_evidence_urls, list):
                    urls = additional_evidence_urls

                download_s3_objects_as_zip(urls, f"Individual_{index + 1}_Files.zip")
            else:
                st.write(f"No Files to download for Individual_{index + 1}")


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
        config["credentials"],
        config["cookie"]["name"],
        config["cookie"]["key"],
        config["cookie"]["expiry_days"],
    )
    name, authentication_status, username = authenticator.login("Login", "main")

    if st.session_state["authentication_status"]:
        data = st.selectbox(
            "Option",
            (
                "See Full Database",
                "View and Download Individual Testimonies and Evidence",
                "Reset Password",
            ),
        )

        if data == "View and Download Individual Testimonies and Evidence":
            table_ind_page()

        if data == "See Full Database":
            table_full_page()

        elif data == "Reset Password":
            if authenticator.reset_password(username, "Reset password"):
                st.success("Password modified successfully")
                save()

        authenticator.logout("Logout", "main")

    elif st.session_state["authentication_status"] == False:
        st.error("Username/password is incorrect")
    elif st.session_state["authentication_status"] == None:
        st.warning("Please enter your username and password")


if __name__ == "__main__":
    main()
