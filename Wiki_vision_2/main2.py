from groq import Groq
import base64
import os
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()

# Streamlit App Header
st.title("Wiki_Vision AI Tool for Images")
st.subheader("Upload an image or enter an image URL to ask the AI anything!")

# Choose image input method
input_method = st.radio("Choose image input method:", ["Upload Image", "Enter Image URL"])

# Initialize Groq client
client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Encode uploaded image as base64
def encode_image(upload):
    return base64.b64encode(upload.read()).decode('utf-8')

# Get response from Groq
def get_response(prompt, image_source, is_base64=False):
    image_payload = (
        f"data:image/jpeg;base64,{image_source}" if is_base64 else image_source
    )

    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": image_payload},
                    },
                ],
            }
        ],
        temperature=1,
        max_completion_tokens=1024,
        top_p=1,
        stream=False,
        stop=None,
    )
    return response.choices[0].message.content

# Handle image input
image_source = None
is_base64 = False

if input_method == "Upload Image":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)
        image_source = encode_image(uploaded_file)
        is_base64 = True

else:
    image_url = st.text_input("Enter image URL")
    if image_url:
        st.image(image_url, caption="Image from URL", use_column_width=True)
        image_source = image_url

# Get user prompt and generate response
if image_source:
    prompt = st.chat_input("Ask a question about this image...")

    if prompt:
        with st.chat_message("human"):
            st.write(prompt)

        with st.spinner("Thinking..."):
            output = get_response(prompt, image_source, is_base64)

        with st.chat_message("assistant"):
            st.write(output)
