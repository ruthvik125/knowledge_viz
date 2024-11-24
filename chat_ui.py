import streamlit as st
import uuid
import os
import base64
import openai
from dotenv import load_dotenv
from textmodel_demo import get_response

# Load environment variables
load_dotenv()

client = openai.OpenAI(
    api_key=os.environ.get("SAMBANOVA_API_KEY"),
    base_url="https://api.sambanova.ai/v1",
)

# Function to handle user input and display chat history
def handle_userinput(user_question: str) -> None:
    if user_question:
        try:
            with st.spinner('🤖 Thinking...'):
                # Simulated response for demonstration
                resp_text = get_response(client,user_question)
                print(resp_text)
                response = {"answer": f"{resp_text}"}
            
            # Append user and AI responses to chat history
            st.session_state.chat_history.append({"user": user_question, "ai": response['answer']})
        except Exception as e:
            st.error(f'An error occurred while processing your question: {str(e)}')

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(
                f"""
                <div style="
                    background-color: #d9f7be;
                    padding: 10px 15px;
                    border-radius: 10px;
                    color: #333;
                    margin-bottom: 10px;
                ">
                    {message["user"]}
                </div>
                """, unsafe_allow_html=True
            )
        with st.chat_message("ai"):
            st.markdown(
                f"""
                <div style="
                    background-color: #e6f7ff;
                    padding: 10px 15px;
                    border-radius: 10px;
                    color: #333;
                    margin-bottom: 10px;
                ">
                    {message["ai"]}
                </div>
                """, unsafe_allow_html=True
            )

# Main function
def main() -> None:
    st.set_page_config(page_title='Enhanced Chat UI', page_icon='🤖')

    # Initialize session state
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    
    # Page title and welcome message
    st.title('💬 Enhanced Chat UI')

    # Chat input
    user_question = st.chat_input('Type your question here...')
    if user_question:
        handle_userinput(user_question)

# Run the app
if __name__ == '__main__':
    main()
