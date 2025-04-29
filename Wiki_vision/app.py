from groq import Groq
import streamlit as st
from dotenv import load_dotenv
import ghana_nlp
import os

st.title("Wiki_Vision AI Tool for Images")
st.subheader("Welcome to the best AI Image Tool")
prompt = st.chat_input("Upload any image ")

load_dotenv()


client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

def get_response(prompt):
    response = client.chat.completions.create(
    model="meta-llama/llama-4-scout-17b-16e-instruct",
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": "What's in this image?"
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": prompt
                    }
                }
            ]
        }
    ],
    temperature=1,
    max_completion_tokens=1024,
    top_p=1,
    stream=False,
    stop=None,
    )

    return response.choices[0].message.content

if prompt:
    with st.chat_message("human"):
        st.write(prompt)
    output = get_response(prompt)
    with st.chat_message("assistant"):
        st.write(output)


