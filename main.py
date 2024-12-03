import streamlit as st
import base64
import math
import requests
import re


st.set_page_config(page_title="Snowflake Pricing Calculator", page_icon="hevo_logo.png")

# Apply Hevo branding and layout changes
st.markdown(
    """
    <style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Source+Sans+Pro:wght@400;600&display=swap');

[data-testid="stToolbar"] {
        visibility: hidden;
        height: 0;
    }

.stApp {
    background-color: white;
    padding-top: 20px;
    overflow: hidden;  /* Prevent scrollbars */
}
.block-container {
        padding: 0rem 0rem 2rem 0rem; /* Adjust padding to minimize height */
    }


.stButton>button {
    background-color: #FF7D42;
    color: white;
    font-size: 14px;
    font-family: 'Source Sans Pro', sans-serif;
    font-weight: bolder;
    padding: 4px 20px;
    border-radius: 8px;
    border: none;
    transition: 0.3s ease;
    margin: 10px;
    margin-top: 26px;
}

.stButton>button:hover {
    background-color: #E06D36;
}

.stButton>button:disabled {
    border: 2px solid #FF7D42;
    background-color: #FFFFFF;
    color: #FF7D42 !important;
}

.stButton>button:active, 
.stButton>button:focus, 
.stButton>button:hover {
    color: white !important;
    background-color: #E06D36 !important;
}

.title-text {
    font-family: 'Source Sans Pro', sans-serif;
    font-size: 36px;
    font-weight: bold;
    color: #333;
    text-align: center;
    margin-bottom: 20px;
}

.result-container, .cta-container {
    font-size: 20px;
    font-weight: bold;
    font-family: 'Inter', sans-serif;
    text-align: center;
    padding: 20px;
    border: 2px solid #FF7D42;
    border-radius: 10px;
    background-color: #FFF5F0;
    margin-top: 20px;
}

.row-widget stButton:hover {
    color: #FFFFFF !important;
}

.cta-container {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
}

.cta-container2 {
    display: flex;
    flex-direction: column; /* Stack elements vertically on smaller screens */
    align-items: flex-start; /* Align items to the left */
    justify-content: center;
    background-color: white;
    border: 1px solid #E3E3E3;
    border-radius: 16px;
    padding: 12px 20px;
    margin-top: 10px;
    gap: 12px; /* Add spacing between text and buttons */
}

.cta-text {
    font-size: 18px; /* Adjust text size for smaller screens */
    color: #333;
    font-family: 'Inter', sans-serif;
    text-align: left;
    margin-bottom: 10px; /* Add spacing below the text */
}

.cta-text1 {
    font-size: 18px;
    color: #333;
    font-family: 'Source Sans Pro', sans-serif;
    font-weight: bold;
    text-align: left;
}

.cta-buttons {
    display: flex;
    flex-direction: column; /* Stack buttons vertically on smaller screens */
    width: 100%; /* Make buttons take full width */
}

.cta-buttons:hover {
    color: white !important;
}

.cta-button1 {
    white-space: nowrap;
    background-color: #FF7D42;
    color: white !important;
    font-size: 14px;
    font-family: 'Source Sans Pro', sans-serif;
    font-weight: bold;
    padding: 12px 20px;
    text-align: center;
    border-radius: 8px;
    margin-bottom: 10px; /* Add space between buttons */
    text-decoration: none;
    transition: 0.3s;
    width: 100%; /* Full width on small screens */
}

.cta-button1:hover {
    background-color: #E06D36;
    text-decoration: none !important;
}

.cta-button2 {
    white-space: nowrap;
    background-color: #FF7D421A;
    color: #FF7D42 !important;
    font-size: 14px;
    font-family: 'Source Sans Pro', sans-serif;
    font-weight: bold;
    padding: 12px 20px;
    text-align: center;
    border-radius: 8px;
    margin-bottom: 10px; /* Add space between buttons */
    text-decoration: none;
    transition: 0.3s;
    width: 100%; /* Full width on small screens */
}

.cta-button2:hover {
    background-color: #FF7D42;
    color: white !important;
    text-decoration: none !important;
}

.rounded-banner {
    width: 100%;
    border-radius: 20px;
}

.result-content {
    display: flex;
    justify-content: space-between;
    padding: 10px 20px;
}

.st-emotion-cache-uzeiqp img {
    max-width: fit-content;
    margin-left: auto;
}

.st-emotion-cache-uzeiqp {
    font-family: "Source Sans Pro", sans-serif;
}

@media (min-width: 768px) {
    .cta-container2 {
        flex-direction: row; /* Arrange elements horizontally on larger screens */
        align-items: center;
        justify-content: space-between;
    }

    .cta-buttons {
        flex-direction: row; /* Arrange buttons side by side on larger screens */
        width: auto; /* Remove full width on larger screens */
    }

    .cta-button1, .cta-button2 {
        width: auto; /* Remove full width on larger screens */
        margin-bottom: 0; /* Remove extra spacing between buttons */
        margin-right: 10px; /* Add spacing between buttons */
    }

    .cta-text {
        margin-bottom: 0; /* Align with buttons on larger screens */
    }
}
</style>
    """,
    unsafe_allow_html=True
)
st.markdown(
    """
    <head>
        <meta name="title" content="Snowflake Cost Calculator for 2025| Hevo">
        <meta name="description" content="Calculate your Snowflake costs quickly and easily. Use Hevo's free calculator to estimate yearly compute and storage costs.">
        <meta name="keywords" content="Snowflake Cost Calculator, Cloud Data Warehouse, Hevo, Snowflake Costs, Snowflake Pricing, Snowflake Pricing Calculator">
        <meta name="author" content="Hevo Data">
    </head>
    """,
    unsafe_allow_html=True
)

# Add the top banner image
st.image('Banner.png', use_column_width=True)

# Function to calculate Snowflake costs
def calculate_cost(warehouse_multiplier, runtime_minutes, cost_per_credit, multiplier_value, storage_gb, transfer_gb):
    runtime_minutes = 0 if math.isnan(runtime_minutes) else runtime_minutes
    cost_per_credit = 0 if math.isnan(cost_per_credit) else cost_per_credit
    storage_gb = 0 if math.isnan(storage_gb) else storage_gb
    transfer_gb = 0 if math.isnan(transfer_gb) else transfer_gb

    # Compute cost calculation
    compute_cost = (warehouse_multiplier * runtime_minutes / 60) * cost_per_credit
    yearly_compute_cost = compute_cost * multiplier_value if multiplier_value else compute_cost

    # Storage cost calculation in GB
    storage_cost_per_gb = 40 / 1024  # Convert $40 per TB to per GB
    transfer_cost_per_gb = 0.02  # Assumes $0.02 per GB transferred across regions
    monthly_storage_cost = storage_gb * storage_cost_per_gb
    monthly_transfer_cost = transfer_gb * transfer_cost_per_gb
    yearly_storage_cost = (monthly_storage_cost + monthly_transfer_cost) * 12


    # Total cost
    yearly_total_cost = yearly_compute_cost + yearly_storage_cost

    return compute_cost, yearly_compute_cost, yearly_storage_cost, yearly_total_cost

# Streamlit UI with side-by-side layout
col1, col2 = st.columns(2)

# Left column inputs
with col1:
    warehouse_size = st.selectbox("Choose a warehouse size:", 
                                  [("XSMALL", 1), ("SMALL", 2), ("MEDIUM", 4), ("LARGE", 8), 
                                   ("XLARGE", 16), ("XXLARGE", 32), ("XXXLARGE", 64),
                                   ("X4LARGE", 128), ("X5LARGE", 256), ("X6LARGE", 512)],
                                  format_func=lambda x: x[0])
    cost_per_credit = st.number_input("Enter your cost per credit (default is $2.00):", min_value=0.0, value=2.00)
    storage_gb = st.number_input("Enter storage capacity in GB:", min_value=0.0, value=1024.0)  # Default set to 1 TB in GB

# Right column inputs
with col2:
    runtime_minutes = st.number_input("Enter the query runtime in minutes:", min_value=0, value=60)
    multiplier_label = {
        "": "None",
        "Hourly": "Hourly",
        "Daily": "Daily",
        "Weekly": "Weekly",
        "Monthly": "Monthly"
    }
    multiplier = st.selectbox("Choose how often your query runs (optional):", 
                              ["", "Hourly", "Daily", "Weekly", "Monthly"],
                              format_func=lambda x: multiplier_label[x])
    transfer_gb = st.number_input("Enter data transfer volume in GB:", min_value=0.0, value=10.0)

# Information box
st.warning('Cost estimates depend on various factors such as cloud provider, region, and data transfer.')

# # Email input and calculate button side-by-side
# email_col, button_col = st.columns([3, 1])
# email = email_col.text_input("", placeholder="Enter Your Company Email")
# calculate_button_disabled = not bool(email)
# Regex for the email validation
# Regex for email validation


domain_regex = re.compile(r"@(?!(gmail|googlemail|hotmail|live|msn|outlook|yahoo|ymail|aol|rediff|icloud|me|mac|yahoomail)\.)")
email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

# Streamlit UI
email_col, button_col = st.columns([3, 1])
email = email_col.text_input("", placeholder="Enter Your Company Email", key="email_input")

# Check if the email matches the regex
is_valid_format = email_regex.match(email) is not None and domain_regex.search(email) is not None

# Disable the button if the email is invalid or empty
calculate_button_disabled = not is_valid_format

# Display feedback if the email format is invalid
if email and not is_valid_format:
    st.error("Invalid email format. Please use your business email (e.g., @yourcompany.com).")

from dotenv import load_dotenv
import os

load_dotenv()

# Webhook URL
webhook_url = os.getenv("WEBHOOK_URL_") # Your webhook URL
# Calculate costs
if button_col.button("Calculate Now", disabled=calculate_button_disabled):
    warehouse_multiplier = warehouse_size[1]
    multiplier_value = {
        "None": 0,
        "Hourly": 8760,
        "Daily": 365,
        "Weekly": 52,
        "Monthly": 12
    }.get(multiplier, 1)

    compute_cost, yearly_compute_cost, storage_cost, yearly_total_cost = calculate_cost(
        warehouse_multiplier, runtime_minutes, cost_per_credit, multiplier_value, storage_gb, transfer_gb
    )

    # Send email to the webhook
    if email:
        try:
            response = requests.post(webhook_url, json={"email": email})
            if response.status_code == 200:
                print("Email sent successfully!")
            else:
                print(f"Failed to send email. Status code: {response.status_code}")
        except Exception as e:
            print(f"Error sending email: {e}")

    st.markdown(f'''
    <div class="result-container">
        <div class="result-content" style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <p style="font-size: 18px; font-weight: normal; margin: 0;">Compute Cost per Run</p>
                <p style="font-size: 28px; font-weight: bold; color: #FF7D42; margin: 0;">${compute_cost:.2f}</p>
            </div>
            <div style="border-left: 2px solid #FFB797; height: 80px; margin: 0 20px;"></div>
            <div>
                <p style="font-size: 18px; font-weight: normal; margin: 0;">Yearly Compute Cost</p>
                <p style="font-size: 28px; font-weight: bold; color: #FF7D42; margin: 0;">${yearly_compute_cost:.2f}</p>
            </div>
        </div>
        <div class="result-content" style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <p style="font-size: 18px; font-weight: normal; margin: 0;">Yearly Storage Cost</p>
                <p style="font-size: 28px; font-weight: bold; color: #FF7D42; margin: 0;">${storage_cost:.2f}</p>
            </div>
            <div style="border-left: 2px solid #FFB797; height: 80px; margin: 0 20px; padding-right: 12px;"></div>
            <div>
                <p style="font-size: 18px; font-weight: normal; margin: 0;">Total Yearly Cost</p>
                <p style="font-size: 28px; font-weight: bold; color: #FF7D42; margin: 0;">${yearly_total_cost:.2f}</p>
            </div>
        </div>
    </div>
''', unsafe_allow_html=True)


# CTA section with text, buttons on left, image on right
# Load the local SVG file and encode it
file_path = "sources_to_snowflake.svg"
with open(file_path, "rb") as file:
    contents = file.read()
data_url = base64.b64encode(contents).decode("utf-8")

st.markdown(f'''
    <div class="cta-container2">
        <div style="text-align: left;">
            <p class="cta-text1">Start Your Data Migration Journey for Free with Hevo!</p>
            <div class="cta-buttons">
                <a href="https://hevodata.com/signup/?step=email&utm_source=SPC&utm_medium=web&utm_campaign=calc" class="cta-button1">Start for Free</a>
                <a href="https://hevodata.com/schedule-demo/?step=email&utm_source=SPC&utm_medium=web&utm_campaign=calc" class="cta-button2">Schedule a Demo</a>
            </div>
        </div>
        <div>
            <img src="data:image/svg+xml;base64,{data_url}" alt="multiple sources" class="rounded-banner" max-width: 200px;">
        </div>
    </div>
''', unsafe_allow_html=True)
