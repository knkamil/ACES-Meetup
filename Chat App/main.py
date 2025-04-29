from groq import Groq
import os
from dotenv import load_dotenv
import streamlit as st
import ghana_nlp 

#streamlit components
st.title("AI Tool for Learners")
st.subheader("This is a demo for interacting with the GROQ API with steamlit.")
prompt = st.chat_input("Ask me anything..")

load_dotenv()

key = os.getenv("GROQ_API_KEY")

client = Groq(api_key= key)

def take_response(prompt):
    #Call the Groq API to get a response
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "you are a helpful assistant."
            },
            # Set a user message for the assistant to respond to.
            {
                "role": "user",
                "content": prompt,
            }
        ],

        # The language model which will generate the completion.
        model="llama-3.3-70b-versatile",

        #
        # Optional parameters
        #

        # Controls randomness: lowering results in less random completions.
        # As the temperature approaches zero, the model will become deterministic
        # and repetitive.
        temperature=0.5,

        # The maximum number of tokens to generate. Requests can use up to
        # 32,768 tokens shared between prompt and completion.
        max_completion_tokens=1024,

        # Controls diversity via nucleus sampling: 0.5 means half of all
        # likelihood-weighted options are considered.
        top_p=1,

        # A stop sequence is a predefined or user-specified text string that
        # signals an AI to stop generating content, ensuring its responses
        # remain focused and concise. Examples include punctuation marks and
        # markers like "[end]".
        stop=None,

        # If set, partial message deltas will be sent.
        stream=False,
    )

    return response.choices[0].message.content

if prompt:
    with st.chat_message("human"):
        st.write(prompt)
    output = take_response(prompt)
    with st.chat_message("assistant"):
        st.write(output)