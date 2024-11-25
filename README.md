# Mindmap Generator and Summarizer

Demo Link: https://nddgy4enmjtv9y4m5hvsfe.streamlit.app

## Project Overview
This project leverages a Large Language Model (LLM) agent to generate summaries and mindmaps from provided content. The application is designed to extract data from a given URL, process it, and provide both textual and visual representations of the information.

---

## Features
1. **Data Scraping**  
   - Extracts content from a specified URL.  
   - Stores the scraped data for further processing.

2. **Summary Generation**  
   - Uses the LLM to create a concise summary of the extracted content.  
   - Provides key highlights for quick understanding.

3. **Mindmap Generation**  
   - Employs the LLM to produce a structured mindmap or graph based on the content.  
   - Visualizes relationships and key concepts for better comprehension.

---

## Workflow
1. **Input URL**  
   The user provides a URL as input.  

2. **Data Scraping**  
   The system scrapes the webpage content and stores it in a structured format.  

3. **LLM Summary**  
   The stored content is processed by the LLM to generate a text-based summary.  

4. **Mindmap Creation**  
   The LLM generates a mindmap or graph that represents the main ideas and relationships derived from the content.  

---

## Use Cases
- Research and note-taking.  
- Content visualization and idea organization.  
- Rapid comprehension of lengthy or complex material.  

---

## Dependencies
- Web scraping libraries (e.g., BeautifulSoup, Requests).  
- LLM API integration.  
- Visualization tools for graph and mindmap generation.  

---

## Future Enhancements
- Support for additional data formats (e.g., PDFs, documents).  
- Interactive mindmap editing.  
- Multi-language support for summaries and mindmaps.  
