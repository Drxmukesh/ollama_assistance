import streamlit as st
import requests
import json
import webbrowser

# Simulated user database
USERS = {"admin": "password"}  # Replace with a secure authentication system

# Session state for authentication
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

# Authentication UI
def login_page():
    st.title("Login to Ollama UI")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username in USERS and USERS[username] == password:
            st.session_state["authenticated"] = True
            st.session_state["username"] = username
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password")
    if st.button("Sign Up"):
        signup_page()

# Signup UI
def signup_page():
    st.title("Sign Up for Ollama UI")
    new_username = st.text_input("New Username")
    new_password = st.text_input("New Password", type="password")
    if st.button("Register"):
        if new_username in USERS:
            st.error("Username already exists")
        else:
            USERS[new_username] = new_password
            st.success("Account created! Please login.")
            login_page()

# Function to fetch data from the internet
def fetch_and_summarize(query):
    search_url = f"https://www.googleapis.com/customsearch/v1?q={query}&key=YOUR_API_KEY&cx=YOUR_CX_ID"
    response = requests.get(search_url)
    if response.status_code == 200:
        results = response.json().get("items", [])
        summary = "\n".join([item["snippet"] for item in results[:5]])
        return summary
    return "No relevant data found."

# Main UI for Ollama Interaction
def main_ui():
    st.sidebar.title("Ollama Web UI")
    model = st.sidebar.selectbox("Select Model", ["GPT-4", "Llama-2", "Mistral"])
    
    history = st.session_state.get("history", [])
    st.sidebar.subheader("History")
    for item in history:
        st.sidebar.text(item)
    
    st.title("Chat with Ollama")
    prompt = st.text_area("Enter your message:")
    if st.button("Generate Response"):
        response = f"[Ollama ({model})]: {prompt[::-1]}"  # Placeholder for actual response
        st.session_state.setdefault("history", []).append(response)
        st.write(response)
    
    # Image Generation
    st.subheader("Image Generation")
    img_prompt = st.text_input("Describe your image:")
    if st.button("Generate Image"):
        st.image("https://via.placeholder.com/300", caption="Generated Image")  # Placeholder
    
    # Internet Summarization
    st.subheader("Real-Time Data Summarization")
    query = st.text_input("Enter search query:")
    if st.button("Summarize"):
        summary = fetch_and_summarize(query)
        st.write(summary)

# Render the UI
if not st.session_state["authenticated"]:
    login_page()
else:
    main_ui()
