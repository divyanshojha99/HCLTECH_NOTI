import streamlit as st
import requests
import base64
import time
 
# Use the same secret key as the server
SECRET_KEY = b'sHlkdKj_0-ZJ56RQlQmn8WS1TghwK31ZJ-ZYNcUgXrs='  # Replace with your actual key

# Define ntfy topic
NTFY_TOPIC = "my-hcl"
NTFY_URL = f"https://ntfy.sh/{NTFY_TOPIC}"  # URL for fetching and posting messages
 
def fetch_latest_notification():
    try:
        response = requests.get(NTFY_URL)
        if response.status_code == 200:
            return response.text.encode()
        else:
            return "No new notifications."
    except Exception as e:
        return f"Error: {e}"
 
def send_message(message: str):
    
    requests.post(NTFY_URL, data=message)
    st.success("Message sent!")
 
# Initialize session state for notification history if it doesn't exist
if "notification_history" not in st.session_state:
    st.session_state.notification_history = []
 
st.title("HCL Notif Client")
 
# Manual check for notifications
if st.button("Check for Notifications"):
    message = fetch_latest_notification()
    st.write("### Latest Notification:")
    st.write(message)
 
# Auto-refresh notifications using a checkbox toggle
if st.checkbox("Enable Auto-Refresh", key="auto_refresh_checkbox"):
    # This component forces a rerun every 2000 ms (2 seconds)
    time.sleep(2)
    new_message = fetch_latest_notification()
    # Only append if it's different from the last message in history
    if not st.session_state.notification_history or st.session_state.notification_history[-1] != new_message:
        st.session_state.notification_history.append(new_message)
 
# Display the history of notifications
st.subheader("Notification History")
for msg in st.session_state.notification_history:
    st.write(f"{msg} | Time: {time.strftime('%H:%M:%S')}")
 
st.write("## Chat")
user_input = st.text_input("Enter your message:")
if st.button("Send Message") and user_input:
    send_message(user_input)
