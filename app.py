import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
st.set_page_config(page_title="RISHU AI", page_icon="🤖")

# Setup the AI Brain from Streamlit Secrets
try:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
    # We use the specific 'models/' prefix to avoid the NotFound error
    model = genai.GenerativeModel('models/gemini-1.5-flash')
except Exception as e:
    st.error("RISHU is having trouble connecting to his brain. Check your API Key in Secrets.")

# --- PASSWORD PROTECTION ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 RISHU ACCESS")
    st.markdown("This assistant is private property.")
    pwd = st.text_input("Enter Access Code:", type="password")
    if st.button("Unlock"):
        if pwd == "76208":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Access Denied. Incorrect Code.")
else:
    # --- RISHU INTERFACE ---
    st.title("🤖 RISHU")
    st.caption("Status: Online | Personality: Bold & Intelligent")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat Input
    if prompt := st.chat_input("Speak..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # RISHU'S BOLD PERSONALITY INSTRUCTIONS
        # We wrap the prompt to ensure he stays in character
        system_instruction = (
            "You are RISHU, a bold, highly intelligent, and practical AI assistant. "
            "Your tone is masculine, direct, and no-nonsense. Do not use fluff. "
            "Answer the following query with authority: "
        )
        
        try:
            response = model.generate_content(system_instruction + prompt)
            with st.chat_message("assistant"):
                st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"RISHU encountered an error: {str(e)}")
