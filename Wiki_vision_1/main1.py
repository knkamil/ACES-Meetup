from groq import Groq
import base64
import os
from dotenv import load_dotenv
import streamlit as st

load_dotenv()

# Streamlit components
st.title("Wiki_Vision AI Tool for Images")  
st.subheader("Welcome to the best AI Image Tool")


uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])


client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

# Function to encode the image
def encode_image(upload):
    return base64.b64encode(upload.read()).decode('utf-8')


def get_response(base64_image):
    response = client.chat.completions.create(
        model="meta-llama/llama-4-scout-17b-16e-instruct",
        messages=[
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What's in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                        },
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


if uploaded_file is not None:
    st.image(uploaded_file, caption="Uploaded Image", use_column_width=True)    

    base64_image = encode_image(uploaded_file)
    with st.spinner("Analyzing..."):         
         output = get_response(base64_image)

         st.success("AI Interpretation:")
         st.write(output)    