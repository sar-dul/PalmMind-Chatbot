from PyPDF2 import PdfReader
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain_community.llms import OpenAI
from langchain.chains.question_answering import load_qa_chain

from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Function to create a vector database from a list of PDF files
def create_vector_db(pdf_files):
    text = ""
    # Iterate through each uploaded PDF file
    for pdf in pdf_files:
        pdf_reader = PdfReader(pdf)
        # Extract text from each page of the PDF
        for page in pdf_reader.pages:
            text += page.extract_text()

    # Split the extracted text into chunks
    text_splitter = CharacterTextSplitter(
        separator = "\n",
        chunk_size = 800,
        chunk_overlap = 200,
        length_function = len
    )
    texts = text_splitter.split_text(text)

    # Create a vector database using FAISS and OpenAI embeddings
    db = FAISS.from_texts(texts, OpenAIEmbeddings())
    return db

# Function to get a response from the query using the vector database
def get_response_from_query(db, query, k):
    # Perform similarity search in the vector database
    docs = db.similarity_search(query, k=k)

    # Initialize the language model with a specified temperature
    llm = OpenAI(temperature=0.5)
        
    # Load a question-answering chain
    chain = load_qa_chain(llm=llm, chain_type='stuff')
    
    # Generate a response using the chain
    response = chain.run(question=query, input_documents=docs)
    return response
