from dotenv import load_dotenv
import os
import streamlit as st
import requests
import io
from PIL import Image

# Load environment variables from the .env file
load_dotenv()

# Access the environment variables
api_url = os.getenv('API_URL')
api_key = os.getenv('API_KEY')
headers = {"Authorization": f"Bearer {api_key}"}

def query_stabilitydiff(payload, headers):
    response = requests.post(api_url, headers=headers, json=payload)
    return response.content

with st.sidebar:
    st.title("💬 Chatbot - Text to Image-StabillityDiff")
    st.caption("//https://github.com/theshahjee")

if "messages" not in st.session_state:
    st.session_state["messages"] = [
        {"role": "assistant", "content": "What kind of image do you want me to draw? (example: running cat) "}]
    
for message in st.session_state.messages:
    st.chat_message(message["role"]).write(message["content"])
    if "image" in message:
        st.chat_message("assistant").image(message["image"], caption=message["prompt"], use_column_width=True)

if prompt := st.chat_input():
    # Input prompt
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)

    # Query Stable Diffusion
    image_bytes = query_stabilitydiff({"inputs": prompt}, headers)

    # Return Image
    image = Image.open(io.BytesIO(image_bytes))
    msg = f'here is your image related to "{prompt}"'

    # Show Result
    st.session_state.messages.append({"role": "assistant", "content": msg, "prompt": prompt, "image": image})
    st.chat_message("assistant").write(msg)
    st.chat_message("assistant").image(image, caption=prompt, use_column_width=True)

