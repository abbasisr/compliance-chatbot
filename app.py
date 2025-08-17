import streamlit as st
import anthropic
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set up the page with better styling
st.set_page_config(
    page_title="Government Compliance AI Assistant",
    page_icon="🏛️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for professional look
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #1f4e79 0%, #2d5aa0 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white;
        margin: 0;
    }
    .main-header p {
        color: #e6f3ff;
        margin: 0.5rem 0 0 0;
    }
</style>
""", unsafe_allow_html=True)


# Initialize Claude client
@st.cache_resource
def init_claude():
    return anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))


client = init_claude()

# Professional header
st.markdown("""
<div class="main-header">
    <h1>🏛️ Government Compliance AI Assistant</h1>
    <p>Expert guidance for NIST, FedRAMP, FISMA, OMB Circulars, and federal compliance requirements</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with quick examples
with st.sidebar:
    st.markdown("### 💡 Example Questions")
    if st.button("What is NIST 800-53?"):
        st.session_state.example_query = "What is NIST 800-53 and what are its main control families?"

    if st.button("FedRAMP Requirements"):
        st.session_state.example_query = "What are the key FedRAMP authorization requirements for cloud services?"

    if st.button("Cloud Migration Help"):
        st.session_state.example_query = "I'm migrating a financial system to AWS for a government agency. What compliance frameworks should I consider?"

    st.markdown("---")
    st.markdown("### 📋 Supported Frameworks")
    st.markdown("""
    - **NIST 800-53** - Security Controls
    - **NIST 800-171** - CUI Protection  
    - **FedRAMP** - Cloud Authorization
    - **FISMA** - Federal Security
    - **OMB Circulars** - Federal Policy
    - **TIC 3.0** - Trusted Internet
    - **Zero Trust** - Architecture
    """)


    st.markdown("---")
    st.markdown("*Created by Sobi Abbasi*")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Handle example queries
if "example_query" in st.session_state:
    st.session_state.messages.append({"role": "user", "content": st.session_state.example_query})
    del st.session_state.example_query
    st.rerun()

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Chat input
if prompt := st.chat_input("Ask me about government compliance frameworks, controls, or implementation guidance..."):
    # Add user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Get AI response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing compliance requirements..."):
            try:
                response = client.messages.create(
                    model="claude-sonnet-4-20250514",
                    max_tokens=1500,
                    system="You are a senior government compliance expert with deep expertise in NIST 800-53, NIST 800-171, FedRAMP, FISMA, OMB Circulars, TIC 3.0, and Zero Trust architecture. Provide detailed, actionable guidance that helps organizations achieve and maintain compliance. Include specific control references when relevant and practical implementation advice.",
                    messages=[
                        {"role": "user", "content": prompt}
                    ]
                )
                ai_response = response.content[0].text
                st.write(ai_response)
                st.session_state.messages.append({"role": "assistant", "content": ai_response})
            except Exception as e:
                st.error(f"Error connecting to AI service: {str(e)}")
                st.info("Please check your API configuration or try again.")