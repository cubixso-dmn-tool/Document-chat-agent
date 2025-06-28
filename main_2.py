import streamlit as st 
from ui_utils import add_bg_from_local 
from file_utils import validate_excel, get_file_hash, process_excel 
from embeddings import update_vector_store 
from llm_utils import generate_response 
from langchain_google_genai import ChatGoogleGenerativeAI 
from dotenv import load_dotenv 
import os 
import base64 
from googletrans import Translator

load_dotenv()

def encode_image(image_path): 
    with open(image_path, "rb") as image_file: 
        return base64.b64encode(image_file.read()).decode("utf-8")

# def translate_thai_to_english(text): 
#     translator = Translator() 
#     translated = translator.translate(text, src='th', dest='en') 
#     return translated.text

llm_gemini = ChatGoogleGenerativeAI( model="gemini-2.0-flash", temperature=0, max_tokens=None, timeout=None, max_retries=2, )

# def process_receipt(image_file): 
#     try: # Encode the image 
#         base64_image = encode_image(image_file)

#     # Define the prompt
#         prompt = (
#             "Extract store name, date, amounts and items from this receipt that are in Thai. "
#             "*The Output should be a json*. Do not make up any assumptions, if you are not sure about something, "
#             "just leave it blank. Do not add any extra information or comments."
#         )

#         # Define the messages for the LLM
#         messages = [
#             {
#                 "role": "user",
#                 "content": [
#                     {"type": "text", "text": prompt},
#                     {
#                         "type": "image_url",
#                         "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
#                     }
#                 ]
#             }
#         ]

#         # Invoke the LLM
#         resp = llm_gemini.invoke(messages).content

#         # Translate the response from Thai to English
#         english_text = translate_thai_to_english(resp)

#         return english_text

#     except Exception as e:
#         return f"Error processing receipt: {str(e)}"


def process_receipt(uploaded_file):
    try:
        # Save the UploadedFile to a temporary file
        with open(uploaded_file.name, "wb") as temp_file:
            temp_file.write(uploaded_file.read())
        
        # Encode the image
        base64_image = encode_image(uploaded_file.name)

        # Define the prompt
        prompt = (
            "Extract store name, date, amounts and items from this receipt that are in Thai. "
            "*The Output should be a json*. Do not make up any assumptions, if you are not sure about something, "
            "just leave it blank. Do not add any extra information or comments."
        )

        # Define the messages for the LLM
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                    }
                ]
            }
        ]

        # Invoke the LLM
        resp = llm_gemini.invoke(messages).content

        # Translate the response from Thai to English
        english_text = translate_thai_to_english(resp)

        return english_text

    except Exception as e:
        return f"Error processing receipt: {str(e)}"


import asyncio  # Import asyncio for handling asynchronous calls

async def process_receipt_async(uploaded_file):
    try:
        # Save the UploadedFile to a temporary file
        with open(uploaded_file.name, "wb") as temp_file:
            temp_file.write(uploaded_file.read())

        # Encode the image
        base64_image = encode_image(uploaded_file.name)

        # Define the prompt
        prompt = (
            "Extract store name, date, amounts and items from this receipt that are in Thai. "
            "*The Output should be a json*. Do not make up any assumptions, if you are not sure about something, "
            "just leave it blank. Do not add any extra information or comments."
        )

        # Define the messages for the LLM
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                    }
                ]
            }
        ]

        # Invoke the LLM
        resp = await llm_gemini.invoke(messages)

        # Translate the response from Thai to English
        english_text = translate_thai_to_english(resp.content)

        return english_text

    except Exception as e:
        return f"Error processing receipt: {str(e)}"

def process_receipt(uploaded_file):
    try:
        # Save the UploadedFile to a temporary file
        with open(uploaded_file.name, "wb") as temp_file:
            temp_file.write(uploaded_file.read())

        # Encode the image
        base64_image = encode_image(uploaded_file.name)

        # Define the prompt
        prompt = (
            "Extract store name, date, amounts and items from this receipt that are in Thai. "
            "*The Output should be a json*. Do not make up any assumptions, if you are not sure about something, "
            "just leave it blank. Do not add any extra information or comments."
        )

        # Define the messages for the LLM
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}
                    }
                ]
            }
        ]

        # Invoke the LLM (synchronously)
        response = llm_gemini.invoke(messages)

        # Check and extract content
        if hasattr(response, "content"):
            # Translate the response from Thai to English
            # english_text = translate_thai_to_english(response.content)
            return response.content
        else:
            raise ValueError("Invalid response format from LLM.")

    except Exception as e:
        return f"Error processing receipt: {str(e)}"



def main(): 
    st.set_page_config( page_title="Tesco Insurance Q&A bot", page_icon="\ud83d\udcca", layout="wide", initial_sidebar_state="expanded", )

add_bg_from_local(r"C:\\Users\\Santosh.Kuricheti\\Downloads\\tesco-insurance-and-money-services-logo-1 (1).png")

# Initialize session state
if "processed_files" not in st.session_state:
    st.session_state.processed_files = {}
if "vector_store" not in st.session_state:
    st.session_state.vector_store = None
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Hello! I am Tesco Insurance chatbot. How can I help you today?"}]
if "receipt_output" not in st.session_state:
    st.session_state.receipt_output = None

# Sidebar Components
with st.sidebar:
    st.markdown("""
    <style>
    .block-container .stSidebar > div > div {
        display: flex;
        flex-direction: column;
        justify-content: space-between;
        height: 100%;
    }
    </style>
    """, unsafe_allow_html=True)

    st.header("Activate Q&A Chatbot")
    uploaded_files = st.file_uploader(
        "Upload files to activate chatbot",
        type=["xlsx", "xls"],
        accept_multiple_files=True,
        help="Upload multiple files for combined analysis"
    )

    if uploaded_files:
        for file in uploaded_files:
            if validate_excel(file):
                file_hash = get_file_hash(file)

                if file_hash not in st.session_state.processed_files:
                    with st.spinner(f"Processing {file.name}..."):
                        try:
                            docs = process_excel(file)
                            st.session_state.vector_store = update_vector_store(docs)
                            st.session_state.processed_files[file_hash] = file.name
                            st.success(f"✅ Processed: {file.name}")
                        except Exception as e:
                            st.error(f"❌ Failed {file.name}: {str(e)}")
                else:
                    st.info(f"⏩ Already processed: {file.name}")
            else:
                st.warning(f"⚠️ Invalid format: {file.name}")

    st.divider()

    st.header("Activate Receipt Reader")
    receipt_files = st.file_uploader(
        "Upload receipts",
        type=["jpg", "png", "jpeg", "pdf"],
        accept_multiple_files=True,
        help="Upload receipts for processing"
    )

    # if st.button("Start Receipt Reader"):
    #     if receipt_files:
    #         for receipt_file in receipt_files:
    #             with st.spinner(f"Processing {receipt_file.name}..."):
    #                 st.session_state.receipt_output = process_receipt(receipt_file)
    #     else:
    #         st.warning("Please upload receipt files to proceed.")

    # if st.button("Start Receipt Reader"):
    #     if receipt_files:
    #         for receipt_file in receipt_files:
    #             with st.spinner(f"Processing {receipt_file.name}..."):
    #                 try:
    #                     result = asyncio.run(process_receipt_async(receipt_file))
    #                     st.session_state.receipt_output = result
    #                 except Exception as e:
    #                     st.error(f"Error: {str(e)}")
    #     else:
    #         st.warning("Please upload receipt files to proceed.")
    
    if st.button("Start Receipt Reader"):
        if receipt_files:
            for receipt_file in receipt_files:
                with st.spinner(f"Processing {receipt_file.name}..."):
                    result = process_receipt(receipt_file)
                    st.session_state.receipt_output = result
        else:
            st.warning("Please upload receipt files to proceed.")
    st.divider()

    st.header("Recommendation System")
    if st.button("Start Recommendation"):
        st.info("Recommendation system functionality is not implemented yet.")

# Main Page Content
if st.session_state.receipt_output:
    st.divider()
    st.title("Receipt Reader Output")
    st.markdown(st.session_state.receipt_output)
    
if st.session_state.vector_store:
    st.divider()
    st.title("Q&A bot")

    # Display chat history with markdown
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            if msg["role"] == "assistant":
                st.markdown(msg["content"], unsafe_allow_html=True)
            else:
                st.write(msg["content"])

    # User input
    if query := st.chat_input("Enter your query ..."):
        # Add user message to history
        st.session_state.messages.append({"role": "user", "content": query})

        # Display user message
        with st.chat_message("user"):
            st.write(query)

        # Generate and display assistant response
        with st.chat_message("assistant"):
            with st.spinner("Analyzing..."):
                try:
                    response = generate_response(query, st.session_state.vector_store)
                    st.markdown(response, unsafe_allow_html=True)
                    st.session_state.messages.append({"role": "assistant", "content": response})
                except Exception as e:
                    error_msg = f"Error generating response: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})
else:
    st.info("Please upload files to activate the chatbot.")

if __name__ == "main": 
    main()






