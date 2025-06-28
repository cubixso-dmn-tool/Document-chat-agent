import streamlit as st
from ui_utils import add_bg_from_local
from file_utils import validate_excel, get_file_hash, process_excel
from embeddings import update_vector_store
from llm_utils import generate_response

def main():
    st.set_page_config(
        page_title=" Tesco Insurance Q&A bot",
        page_icon="📊",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    add_bg_from_local(r"C:\Users\Santosh.Kuricheti\Downloads\tesco-insurance-and-money-services-logo-1 (1).png")
    
    # Initialize session state
    if "processed_files" not in st.session_state:
        st.session_state.processed_files = {}
    if "vector_store" not in st.session_state:
        st.session_state.vector_store = None
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "Hello! I am Tesco Insurance chatbot. How can I help you today?"}]
    
    # File Upload & Processing
    with st.sidebar:
        st.header("📂 File Upload")
        uploaded_files = st.file_uploader(
            "Upload files",
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
        st.markdown("# Reciept Reader")
        st.button("Reciept Reader", help="Upload your reciept to get the details of the reciept")
        st.markdown("# Product Recommender")
        st.button("Product Recommedation", help="get the product recommedation based on your reciept")

    # Interactive Q&A
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
        st.info("Please upload files to begin.")

if __name__ == "__main__":
    main()






