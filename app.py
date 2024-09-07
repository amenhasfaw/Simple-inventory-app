import streamlit as st
import logging
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Logging
logging.basicConfig(level=logging.INFO)

# Constants for Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '174S-zyU55VsxIFYsgWid3KqteduKfcu3zxsxIB7jhc0'
CREDENTIALS_PATH = './Cred2.json'
SAMPLE_RANGE_NAME = 'Sheet1!A:C' 

def authenticate():
    try:
        credentials = Credentials.from_service_account_file(CREDENTIALS_PATH, scopes=SCOPES)
        service = build('sheets', 'v4', credentials=credentials)
        return service
    except Exception as e:
        logging.error(f"Failed to authenticate: {e}")
        return None

def read_data_from_spreadsheet(service):
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=SAMPLE_RANGE_NAME).execute()
    values = result.get('values', [])
    if not values:
        logging.info('No data found.')
        return []
    logging.info(values)
    return values

# Streamlit app
st.title("Available Products")

# Authenticate and read data
service = authenticate()
if service:
    data = read_data_from_spreadsheet(service)
    if data:
        for row in data[1:]:
            product_name, availability_status, image_url = row
            
            if availability_status == 'Available':
                
                if image_url and image_url.startswith('http'):
                    st.image(image_url, caption=product_name, width=150)
                else:
                    st.warning(f"Image not available for {product_name}")
