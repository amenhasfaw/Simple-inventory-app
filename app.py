import streamlit as st
import logging
from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Logging
logging.basicConfig(level=logging.INFO)

# Constants for Google Sheets
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = '174S-zyU55VsxIFYsgWid3KqteduKfcu3zxsxIB7jhc0'
CREDENTIALS_PATH = './Credentials.json'
SAMPLE_RANGE_NAME = 'Sheet1!A:C'  # Assuming columns A to C are relevant

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
st.markdown("<h1 style='text-align: center;'>Available Products</h1>", unsafe_allow_html=True)

# Authenticate and read data
service = authenticate()
if service:
    data = read_data_from_spreadsheet(service)
    if data:
        # Add custom CSS to handle mobile view
        st.markdown("""
            <style>
                @media (max-width: 600px) {
                    .image-container {
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                    }
                    .image-item {
                        width: 100%;
                        max-width: 300px; /* Limit max-width of images */
                        margin-bottom: 20px;
                    }
                }
                @media (min-width: 601px) {
                    .image-container {
                        display: flex;
                        flex-wrap: wrap;
                        gap: 10px;
                        justify-content: center;
                    }
                    .image-item {
                        flex: 1 1 45%;
                        max-width: 300px;
                        box-sizing: border-box;
                    }
                    .image-item img {
                        width: 100%;
                        height: auto;
                    }
                }
                .image-item p {
                    text-align: center;
                    margin: 0;
                }
            </style>
            <div class="image-container">
            """, unsafe_allow_html=True)

        # Create columns for desktop view
        num_columns = 2
        columns = st.columns(num_columns)
        column_index = 0

        for row in data[1:]:
            product_name, availability_status, image_url = row
            
            if availability_status == 'Available':
                # Display image and product name in the current column
                with columns[column_index]:
                    st.image(image_url, caption=product_name, use_column_width=True)
                
                # Move to the next column, wrap to the first column if needed
                column_index = (column_index + 1) % num_columns

        # Close the flexbox container
        st.markdown("</div>", unsafe_allow_html=True)
