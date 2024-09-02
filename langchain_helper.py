import cohere
from PyPDF2 import PdfReader

# for using in your one machine use your own api key
COHERE_API_KEY = "kOOfj9dMFIKfxtZL9z2CBuMiZn8fgZAkLvbJdlRB"
co = cohere.Client(COHERE_API_KEY)


# Function to create a vector database from a list of PDF files
def extract_text_from_pdfs(pdf_files):
    text = ""
    # Iterate through each uploaded PDF file
    for pdf in pdf_files:
        pdf_reader = PdfReader(pdf)
        # Extract text from each page of the PDF
        for page in pdf_reader.pages:
            text += page.extract_text()

    return text

# Function to get a response from the query using the vector database
def get_query_response(db, query):

    prompt = f"Here are some documents: {db}\n\nQ: {query}\nA:"

    response = co.generate(
            model='command-xlarge-nightly', 
            prompt=prompt,
            max_tokens=150
        )
    return response.generations[0].text.strip()