import langchain_helper as lch
import streamlit as st

# Initialize session state variables
def initialize_session_state():
    if 'db' not in st.session_state:
        st.session_state.db = None
    if 'submitted' not in st.session_state:
        st.session_state.submitted = False
        st.session_state.name = ''
        st.session_state.phone_number = ''
        st.session_state.email = ''
    if 'conversation' not in st.session_state:
        st.session_state.conversation = []

# Set the page configuration for the Streamlit app
def set_page_config():
    st.set_page_config(page_title="Document Query Chatbot", page_icon="🤖", layout="wide")

# Display the title of the app
def display_title():
    st.title("📄 Document Query Chatbot")
    st.write("Upload your documents and ask any question about them.")

# Handle file upload from the sidebar
def handle_file_upload():
    st.sidebar.header("Upload Documents")
    uploaded_files = st.sidebar.file_uploader("Upload PDF files", accept_multiple_files=True)

    if st.sidebar.button("Process Files"):
        if uploaded_files:
            with st.spinner("Processing files..."):
                st.session_state.db = lch.create_vector_db(uploaded_files)
            st.sidebar.success("Files processed successfully!")
        else:
            st.sidebar.warning("Please upload at least one PDF file.")

# Display the input field for user questions
def display_question_input():
    st.subheader("Ask Your Question")
    user_input = st.text_input("Enter your question here:")

    if user_input:
        handle_user_input(user_input)
    else:
        st.warning("Please enter a question.")

# Handle user input, determine if it's a call request or a normal query
def handle_user_input(user_input):
    if "call me" in user_input.lower():
        handle_call_me_request()
    else:
        generate_response(user_input)

# Handle the "call me" request by collecting user details
def handle_call_me_request():
    if not st.session_state.submitted:
        st.session_state.name = st.text_input("Please enter your name:")
        st.session_state.phone_number = st.text_input("Please enter your phone number:")
        st.session_state.email = st.text_input("Please enter your email:")
        st.warning("You cannot change your details once submitted.")
        if st.button("Submit"):
            st.session_state.submitted = True
            st.info(f"Thank you, {st.session_state.name}. We will contact you at {st.session_state.phone_number} or {st.session_state.email}.")
            st.session_state.conversation.append({
                "role": "user",
                "content": "call me"
            })
            st.session_state.conversation.append({
                "role": "system",
                "content": f"Thank you, {st.session_state.name}. We will contact you at {st.session_state.phone_number} or {st.session_state.email}."
            })
            st.rerun()
    else:
        st.info(f"Thank you, {st.session_state.name}. We will contact you at {st.session_state.phone_number} or {st.session_state.email}.")

# Generate a response from the chatbot for the user's query
def generate_response(user_input):
    with st.spinner("Generating response..."):
        response = lch.get_response_from_query(st.session_state.db, user_input, 3)
        st.session_state.conversation.append({"role": "user", "content": user_input})
        st.session_state.conversation.append({"role": "chatbot", "content": response})
        st.text_area("Chatbot Response", value=response, height=200)

# Display the conversation between the user and the chatbot
def display_conversation():
    st.subheader("Conversation")
    for entry in st.session_state.conversation:
        if entry["role"] == "user":
            st.markdown(f"**User:** {entry['content']}")
        elif entry["role"] == "chatbot":
            st.markdown(f"**Chatbot:** {entry['content']}")
        else:
            st.markdown(f"**System:** {entry['content']}")

# Main function to run the Streamlit app
def main():
    set_page_config()
    display_title()
    initialize_session_state()
    handle_file_upload()

    if st.session_state.db:
        display_question_input()
        display_conversation()
    else:
        st.info("Please upload and process your PDF files first.")

if __name__ == "__main__":
    main()
