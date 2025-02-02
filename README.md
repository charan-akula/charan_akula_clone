# AI Clone: Resume and Portfolio Interaction System

Welcome to the **AI Clone** project! This AI-powered assistant was developed to explore and interact with my resume and portfolio, aiming to provide intelligent responses and insights regarding my professional journey.

The project is designed to allow users to ask questions about my work, skills, experiences, and portfolio. It can efficiently retrieve relevant data from the stored documents and provide personalized responses based on the provided information. This project serves as a great showcase of how AI and natural language processing (NLP) can be leveraged for professional and personal branding.

## Key Features:
- **Resume Interaction**: Get details about my career experience, skills, and other important aspects from my resume.
- **Portfolio Interaction**: Learn more about the projects and work I’ve done, providing insights into my creative and technical journey.
- **Intelligent Responses**: The AI model retrieves relevant context from the documents and provides accurate responses based on user queries.
- **Polite Behavior**: The AI maintains a polite and formal tone, ensuring a respectful interaction.

## Technologies Used:
- **Python**: The main programming language for developing the entire AI Clone project.
- **Streamlit**: For creating an interactive web-based user interface to interact with the AI.
- **Langchain**: Used for document processing, natural language understanding, and building the AI query-response pipeline.
- **Large Language Models (LLMs)**: Leveraged to generate human-like responses and handle complex queries.
- **Generative AI**: Built using generative AI models, the system is capable of understanding and responding in a personalized way based on the given context.
- **FAISS/Vector Databases**: For storing and retrieving embeddings of documents efficiently, improving the response time and query accuracy.
- **Cohere API**: Used for generating high-quality document embeddings for better understanding of content.

## Purpose:
The AI Clone was developed with the purpose of helping me better understand and interact with my own professional data. By using the AI Clone, users can ask detailed questions related to my skills, work experience, and projects from my resume and portfolio. The idea behind this project was to not only explore AI technologies but also to make it more personal by reflecting my skills and work history.

## How It Works:
1. **Document Loading**: The resume and portfolio data are loaded from PDFs into a processable format.
2. **Text Splitting and Embeddings**: Text from documents is split into manageable chunks, and embeddings are generated using **Cohere's embedding models**.
3. **FAISS Index**: A **FAISS index** is used to store the embeddings locally for quick and efficient retrieval of relevant information.
4. **LLM Integration**: The AI model responds to user queries about the resume or portfolio, extracting relevant context from the vector store.
5. **Streamlit Interface**: The web-based interface allows users to interact with the AI in a simple, accessible way.

## Installation and Setup:
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/ai-clone.git
2. Install the requirements:
   ```bash
   pip install -r requirements.txt
3. prepare your own data:
   ```bash
   replace my pdf with your data
4. set up the api keys :
   ```bash
   visit cohere and chatgroq websites for api keys
5. Run the project:
   ```bash
   python streamlit run clone.py
