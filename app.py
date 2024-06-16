from dotenv import load_dotenv

load_dotenv()

import streamlit as st
import os
from PIL import Image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


model= genai.GenerativeModel('gemini-pro-vision')


def get_gemini_response(input,image,prompt):
    response=model.generate_content([input,image[0],prompt])
    return response.text

def input_image_details(uploaded_file):
    # Check if a file has been uploaded
    if uploaded_file is not None:
        # Read the file into bytes
        bytes_data = uploaded_file.getvalue()

        image_parts = [
            {
                "mime_type": uploaded_file.type,  # Get the mime type of the uploaded file
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded")



#intialize our streamlit app

st.set_page_config(page_title="MultiLanguage invoice extractor")

st.header("MultiLanguage invoice extractor")

input=st.text_input("input prompt",key="input")
uploaded_file = st.file_uploader("Choose an image of the invoice", type=["jpg","jpeg","png"])
image=""

if uploaded_file is not None:
    image=Image.open(uploaded_file)
    st.image(image, caption="Uploaded Image.",use_column_width=True)

submit =st.button("Tell me about the invoice")

input_prompt="""you are expert in understanding invoices. we will upload an image as invoice
and you will have to answer any question regarding the particular upladed invoice image"""



# if submit button is clicked
image_data=input_image_details(uploaded_file)
response=get_gemini_response(input_prompt,image_data,input)
st.subheader("The response is")
st.write(response)