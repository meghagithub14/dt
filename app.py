from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os 
import io
import base64
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

def get_gemini_response(input , pdf_content ,prompt):
    # model = genai.GenerativeModel('gemini-pro-vision')
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content([input ,pdf_content[0] , prompt])
    return response.text

def input_pdf_setup(uploaded_file):
    if uploaded_file is not None :

        # convert pdf into image
        images = pdf2image.convert_from_bytes(uploaded_file.read())
        first_page = images[0]

        # convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr ,format= 'JPEG')
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type" : "image/jpeg" ,
                "data" : base64.b64encode(img_byte_arr).decode()
            }
        ]

        return pdf_parts
    else :
        raise FileNotFoundError("No File Uploaded")
    

 # STreamlit app
st.set_page_config(page_title="ATS Resume Expeert")
st.header("MY PERSONAL ATS")
input_text = st.text_area("Job Description: " , key ="input")
uploaded_file = st.file_uploader("Upload your resume(PDF)..",type=['pdf'])

if uploaded_file is not None:
    st.write("PDF Uploaded Successfully...")

submit1 =st.button("Tell Me About the Resume")
submit2 =st.button("How can I improvise my skills ")
submit3 =st.button("What are the keywords that are missing ")
submit4 =st.button("Percentage Match")
# submit5 =st.button("")

input_prompt1 ="""
You are an experienced HR with Tech Experience in the field of any job role from Data Science ,Full stack ,
web development ,BIg DAta Engineering ,DEVOPS ,Data Analyst ,Your task is to review the provided resume against 
the job description for these profilrs.
Please Share your professional evaluation on whether the candidate's profie align with Highlights the strenghts and weakness of the applicant in relation to the specified job role
"""

input_prompt4 ="""
You are an skilled ATS(Applicant Tracking System) scanner with a deep understanding of Data Science ,Full Stack ,Web development , Big Data Engineering ,DEVOPS , Data Analyst and deep ATS functionality . Your task is to available the resume against the provided job description . Given me the percentage of match if the resume matches the job decription.
First the output should come as percentage then keywords mising and last final
"""

if submit1:
    if uploaded_file is not None :
        pdf_content =input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt1 ,pdf_content ,input_text)
        st.subheader("The Response is")
        st.write(response)
    else :
        st.write("Please upload the resume")

elif submit4 :
    if uploaded_file is not None :
        pdf_content =input_pdf_setup(uploaded_file)
        response = get_gemini_response(input_prompt4 ,pdf_content ,input_text)
        st.subheader("The Response is")
        st.write(response)
    else :
        st.write("Please upload the resume")

