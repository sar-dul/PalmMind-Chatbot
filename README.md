# PalmMind PDF Chatbot

This project is a chatbot that takes multiple PDF files as inputs and answers questions based on the content of the PDFs. It uses Streamlit for the user interface and LangChain along with Gemini/other LLMs for processing and generating responses.

## Features

- Upload multiple PDF files
- Extract content from PDFs
- Answer questions based on the content of the uploaded PDFs
- Collect user information (Name, Phone Number, Email) upon request

## Installation

1. **Clone the repository:**

    ```bash
    git clone https://github.com/your-username/pdf-chatbot.git
    cd pdf-chatbot
    ```

2. **Create a virtual environment:**

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3. **Install the dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

## Usage

1. **Run the Streamlit app:**

    ```bash
    streamlit run app.py
    ```

2. **Upload PDF files:**

    - Use the file uploader in the Streamlit interface to upload one or more PDF files.

3. **Ask questions:**

    - Enter your questions in the input field. The chatbot will respond based on the content of the uploaded PDFs.

4. **Collect user information:**

    - If you ask the chatbot to call you, it will prompt you to provide your name, phone number, and email.

## File Structure

