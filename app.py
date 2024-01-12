import streamlit as st
import streamlit_authenticator as stauth
import pandas as pd
from sqlalchemy import create_engine
import os
from dotenv import load_dotenv
import yaml
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

def table_page():        
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
                "See Database",
                "Reset Password"
            ),
        )
        
        if data == "See Database":
            table_page()
        
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
    # hashed_passwords = stauth.Hasher(['password', 'def']).generate()
    # print(hashed_passwords)
