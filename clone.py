import streamlit as st
from fpdf import FPDF # for converting the text into pdf 
import base64

def get_base64_image(image_path):
    """Converts an image file to a base64 encoded string."""
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")

def generate_pdf():
    # Create PDF instance
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    # Set font for the title
    pdf.set_font("Arial", size=16, style='B')
    pdf.cell(200, 10, txt="Chat History", ln=True, align="C")
    pdf.ln(10)

    # Loop through messages to add them to the PDF
    for message in st.session_state.messages:
        if message["role"] == "user":
            # Set red color and bold font for the user heading
            pdf.set_text_color(255, 0, 0)  # Red color for headings
            pdf.set_font("Arial", "B", 12)  # Bold font for user headings
            pdf.cell(0, 10, "User:", ln=True)

            # Set black color and normal font for the user message content
            pdf.set_text_color(0, 0, 0)  # Black color for content
            pdf.set_font("Arial", "", 12)  # Normal font for user content
            pdf.multi_cell(0, 10, message["content"])

        elif message["role"] == "system":
            # Set red color and bold font for the system heading
            pdf.set_text_color(255, 0, 0)  # Red color for headings
            pdf.set_font("Arial", "B", 12)  # Bold font for system headings
            pdf.cell(0, 10, "System:", ln=True)

            # Set black color and normal font for the system message content
            pdf.set_text_color(0, 0, 0)  # Black color for content
            pdf.set_font("Arial", "", 12)  # Normal font for system content
            pdf.multi_cell(0, 10, message["content"])

        # Add a small gap between each message
        pdf.ln(5)

    # Output the PDF to a binary stream (for download)
    pdf_output = pdf.output(dest='S').encode('latin1')
    return pdf_output

if "messages" not in st.session_state:
    st.session_state.messages = []

# Paths to images
user_logo = "data/user.jpeg"
system_logo = "data/passphoto.jpg"

# Display title and description
st.title("I'm Charan")
st.markdown('<p style="color: blue;">I am actually an AI clone of A. Sai Charan, developed by himself, '
            'to assist the user in knowing better about his resume, portfolio, and much more. Feel free to '
            'know about him.</p>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)  # Horizontal line below text

# Function to display chat history with avatars
# Function to display chat messages with avatars
def display_messages():
    for message in st.session_state.messages:
        avatar = user_logo if message["role"] == "user" else system_logo
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])


import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Access the API keys from the environment variables
cohere_api_key = os.getenv("COHERE_API_KEY")
groq_api_key = os.getenv("GROQ_API_KEY")

from langchain_cohere import CohereEmbeddings
new_embeddings = CohereEmbeddings(model="embed-english-v3.0", cohere_api_key=None)

from langchain_community.vectorstores import FAISS
loaded_db = FAISS.load_local("faiss_store",new_embeddings,allow_dangerous_deserialization=True)
retriever = loaded_db.as_retriever(
    search_type="similarity", search_kwargs={"k":3}
)
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
llm=ChatGroq(   # model
    temperature=0.4, 
    groq_api_key=groq_api_key,
    model_name="llama-3.3-70b-versatile",
    max_tokens=None)
system_prompt=("Iam charan You are a AI Clone of a A Sai charan , developed by himself better resume and portfolio interaction "
               "You are trained only for resume and portfolio queries only and you should not answer any personal questions that you dont know "
                "Follow polite behavior for greeting and answering the questions"
               "answer the queries based in the context or data that is retived from vector store"
               "if you dont any answer politely say that i don't know and give my email ID charanakula.632@gmail.com to contact me"
               "if any personl or sensitive questions were asked say that iam not supposed to answer them"
               "if user asks to tell me your self or tell me your skills dont add any extra points for that  just give what i mentioned in document"
               "{context}"
               
              ) ## conetxt is autofilled
template=ChatPromptTemplate.from_messages(
    [("system",system_prompt),
    ("human","{input}"),
    ("ai","")]
)
from langchain.chains.combine_documents import create_stuff_documents_chain # This chain takes a list of documents and formats them all into a prompt, then passes that prompt to an LLM. 
from langchain.chains import create_retrieval_chain

question_answer_chain = create_stuff_documents_chain(llm,template)
rag_chain = create_retrieval_chain(retriever, question_answer_chain) # here 1st chunks are retrived and then it was combined with prompt to get response from llm


# Predefined buttons (always visible)
if st.button("Introduce about yourself"):
    user_op = rag_chain.invoke({"input": "tell me about your self"})["answer"]
    st.session_state.messages.append({"role": "user", "content": "Introduce about yourself"})
    st.session_state.messages.append({"role": "bot", "content": user_op})

if st.button("What are your skills?"):
    user_opp =rag_chain.invoke({"input": "what are your skills"})["answer"]

    st.session_state.messages.append({"role": "user", "content": "What are your skills"})
    st.session_state.messages.append({"role": "bot", "content": user_op})

if st.button("What is your educational background?"):
    user_op =rag_chain.invoke({"input": "what is your educational background"})["answer"]
    st.session_state.messages.append({"role": "user", "content": "What is your educational background?"})
    st.session_state.messages.append({"role": "bot", "content": user_op})

# Get user input and process it
user_input = st.chat_input("Type your message:")

if user_input:
    # Append user input to session state as a message
    st.session_state.messages.append({"role": "user", "content": user_input})

    # Generate bot's response (same as user input, can be modified)
    bot_response =rag_chain.invoke({"input":user_input})["answer"]


    # Append bot's response as message
    st.session_state.messages.append({"role": "bot", "content": bot_response})

    # Display updated chat history
    display_messages()

else:
    # If no user input, just display the messages
    display_messages()

# Sidebar to clear the chat history

if len(st.session_state.messages) > 0:
    if st.sidebar.button("Clear History"):
        st.session_state.messages = []  # Reset the chat history
else:
    st.sidebar.write("No history to clear")

if len(st.session_state.messages) > 0:
    # Generate the PDF
    pdf_file = generate_pdf()

    # Show the download button only if there is chat history
    st.sidebar.download_button(
        label="Download History",
        data=pdf_file,
        file_name="chat_history.pdf",
        mime="application/pdf",
        key="download_pdf_button"
    )
else:
    # Display a message when there is no chat history
    st.sidebar.write("No history to download")

