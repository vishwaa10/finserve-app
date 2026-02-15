import streamlit as st
from pypdf import PdfReader
from openai import OpenAI

st.set_page_config(page_title="FinServe Analyst Tool")

st.title("📊 FinServe: Earnings Call Analyzer")
st.markdown("Upload a PDF transcript to extract Management Sentiment, Risks, and Guidance.")

# Sidebar for API Key
with st.sidebar:
    st.header("Setup")
    api_key = st.text_input("Enter OpenAI API Key", type="password")
    st.info("The key is strictly used for processing and not stored.")

# Function to read PDF
def get_pdf_text(uploaded_file):
    text = ""
    try:
        reader = PdfReader(uploaded_file)
        for page in reader.pages:
            text += page.extract_text()
        return text
    except:
        return ""

uploaded_file = st.file_uploader("Upload PDF", type="pdf")

if uploaded_file and api_key:
    if st.button("Run Analysis"):
        with st.spinner("Analyzing document... (This may take 10-20 seconds)"):
            try:
                # 1. Get Text
                text = get_pdf_text(uploaded_file)
                
                # 2. Call AI
                client = OpenAI(api_key=api_key)
                prompt = f"""
                Act as a financial analyst. Analyze this text and output the following in Markdown:
                1. **Management Sentiment**: Score (1-10) and Tone.
                2. **Top 3 Risks**: Bullet points.
                3. **Forward Guidance**: Create a table with Revenue, Margin, and Capex outlooks.
                
                Text: {text[:15000]}
                """
                
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                # 3. Show Result
                st.markdown("---")
                st.markdown(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"Error: {e}. Check your API Key.")
elif uploaded_file and not api_key:
    st.warning("Please enter your OpenAI API Key in the sidebar to run the tool.")
