import streamlit as st
import uuid
import os
import base64
import openai
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO
import requests
from textmodel_demo import get_response
import re
from custom_summary import recursive_summarization
from langchain.document_loaders import WebBaseLoader

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = openai.OpenAI(
    api_key=os.environ.get("SAMBANOVA_API_KEY"),
    base_url="https://api.sambanova.ai/v1",
)

# Function to extract Mermaid code from the response
def extract_mermaid_code(response):
    match = re.search(r"```mermaid\n(.*?)```", response, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None

# Function to generate Mermaid graph
def generate_mermaid_graph(graph):
    graphbytes = graph.encode("utf8")
    base64_bytes = base64.urlsafe_b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    image_url = "https://mermaid.ink/img/" + base64_string
    
    response = requests.get(image_url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        st.error(f"Failed to fetch image. HTTP Status Code: {response.status_code}")
        return None

# Function to fetch document content from a URL
def fetch_document(url):
    """Fetches a document from the specified URL."""
    loader = WebBaseLoader(url)
    docs = loader.load()
    return " ".join(doc.page_content for doc in docs)

# Function to handle user input and display chat history
def handle_userinput(user_question: str,diagram_type_option:str, input_data: str = None) -> None:
    if user_question:
        try:
            with st.spinner('🤖 Summarizing the input...'):
                # Summarize input data (code or document content)
                summary = recursive_summarization(client,input_data) if input_data else None
                #st.info(f"Summary:\n{summary}")

            
            modified_question_for_diagram_type = (
                f"For this summary, which Mermaid diagram is suitable?\n{summary}\n"
                "Options: Flowchart, Sequence Diagram, Class Diagram, State Diagram, Entity Relationship Diagram, "
                "User Journey, Gantt, Pie Chart, Quadrant Chart, Requirement Diagram, Gitgraph (Git) Diagram, "
                "C4 Diagram, Mindmaps, Timeline, ZenUML, Sankey, XY Chart, Block Diagram, Packet, Kanban, Architecture"
            )
           

# Modify the logic to determine the diagram type
            if diagram_type_option == "Automatic Detection":
                with st.spinner('🤖 Determining the diagram type...'):
                    modified_question_for_diagram_type = (
                        f"For this summary, which Mermaid diagram is suitable?\n{summary}\n"
                        "Options: Flowchart, Sequence Diagram, Class Diagram, State Diagram, Entity Relationship Diagram, "
                        "User Journey, Gantt, Pie Chart, Quadrant Chart, Requirement Diagram, Gitgraph (Git) Diagram, "
                        "C4 Diagram, Mindmaps, Timeline, ZenUML, Sankey, XY Chart, Block Diagram, Packet, Kanban, Architecture"
                    )
                    resp_text = get_response(client, modified_question_for_diagram_type)
                    diagram_type = resp_text.strip()  # Infer the type from the model
            else:
                diagram_type = diagram_type_option  # Use the type selected by the user

            
            
            # Modify user question to include the summary for generating a Mermaid graph
            modified_question = (
                f"{user_question}\nBased on the following summary, generate a Mermaid {diagram_type}:\n{summary}.OUTPUT must only contain the mermaid code with proper formatting for the syntax"
            )

            with st.spinner('🤖 Generating response...'):
                # Get response from model
                resp_text = get_response(client, modified_question)
                response = {"answer": f"{resp_text}"}

            # Extract and generate Mermaid graph
            mermaid_code = extract_mermaid_code(response['answer'])
            if mermaid_code:
                st.info("Rendering graph...")
                graph_image = generate_mermaid_graph(mermaid_code)
                if graph_image:
                    # Use columns to display summary and graph side by side
                    col1, col2 = st.columns([1, 1])  # Create two columns
                    with col1:
                        st.info("Summary:")
                        st.write(summary)  # Display the summary in the first column
                    with col2:
                        st.image(graph_image, caption="Generated Mermaid Graph")  # Display the diagram in the second column
                else:
                    st.warning("Failed to generate graph.")

        except Exception as e:
            st.error(f"An error occurred while processing your question: {str(e)}")

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(
                f"""
                <div style="background-color: #d9f7be; padding: 10px 15px; border-radius: 10px; color: #333; margin-bottom: 10px;">
                    {message["user"]}
                </div>
                """,
                unsafe_allow_html=True,
            )
        with st.chat_message("ai"):
            st.markdown(
                f"""
                <div style="background-color: #e6f7ff; padding: 10px 15px; border-radius: 10px; color: #333; margin-bottom: 10px;">
                    {message["ai"]}
                </div>
                """,
                unsafe_allow_html=True,
            )

# Main function
def main() -> None:
    st.set_page_config(page_title='Chat + Mermaid UI', page_icon='🤖', layout="wide")

    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    st.title('💬 Chat UI')

    # Dropdown to choose input method
    input_option = st.selectbox(
        "Choose an input method:",
        options=["Upload a Code File", "Paste a URL"]
    )

    input_data = None

    if input_option == "Upload a Code File":
        uploaded_file = st.file_uploader("Upload your code file", type=["py", "txt", "cpp", "java", "js"])
        if uploaded_file:
            input_data = uploaded_file.read().decode("utf-8")
            st.text_area("Code Preview", value=input_data, height=300, disabled=True)

    elif input_option == "Paste a URL":
        url = st.text_input("Paste the URL here:")
        if url:
            try:
                with st.spinner('Fetching document...'):
                    input_data = fetch_document(url)
                    st.text_area("Document Content", value=input_data, height=300, disabled=True)
            except Exception as e:
                st.error(f"Failed to fetch document: {str(e)}")

    diagram_type_option = st.selectbox(
            "Select the diagram type:",
            options=["Automatic Detection", "Flowchart", "Sequence Diagram", "Class Diagram", "State Diagram",
                    "Entity Relationship Diagram", "User Journey", "Gantt", "Pie Chart", "Quadrant Chart",
                    "Requirement Diagram", "Gitgraph (Git) Diagram", "C4 Diagram", "Mindmaps", "Timeline",
                    "ZenUML", "Sankey", "XY Chart", "Block Diagram", "Packet", "Kanban", "Architecture"]
        )
    
    
    if st.button('Generate Visual Summary'):
        user_question = "st.text_input('Type your question here...')"
        
        if user_question:
                handle_userinput(user_question,diagram_type_option, input_data=input_data)

if __name__ == '__main__':
    main()
