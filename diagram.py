import base64
import requests
from PIL import Image
from io import BytesIO
import streamlit as st

def generate_mermaid_graph(graph):
    # Convert graph definition to base64 string
    graphbytes = graph.encode("utf8")
    base64_bytes = base64.urlsafe_b64encode(graphbytes)
    base64_string = base64_bytes.decode("ascii")
    
    # Construct Mermaid image URL
    image_url = "https://mermaid.ink/img/" + base64_string
    
    # Fetch the image
    response = requests.get(image_url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        st.error(f"Failed to fetch image. HTTP Status Code: {response.status_code}")
        return None

# Streamlit UI
st.title("Mermaid Graph Viewer")
st.write("Enter a Mermaid graph definition below to generate and view the graph.")

# Text area for Mermaid input
mermaid_input = st.text_area("Mermaid Graph Definition", height=200, value="""
graph LR;
    A--> B & C & D;
    B--> A & E;
    C--> A & E;
    D--> A & E;
    E--> B & C & D;
""")

if st.button("Generate Graph"):
    # Generate and display the graph
    if mermaid_input.strip():
        graph_image = generate_mermaid_graph(mermaid_input)
        if graph_image:
            st.image(graph_image, caption="Generated Mermaid Graph")
    else:
        st.warning("Please enter a valid Mermaid graph definition.")
