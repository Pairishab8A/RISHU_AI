import streamlit as st
import google.generativeai as genai

# Setup the AI Brain
genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])

# We changed 'gemini-1.5-flash' to 'models/gemini-1.5-flash'
# This is more specific and usually fixes the "NotFound" error.
model = genai.GenerativeModel('models/gemini-1.5-flash')
st.set_page_config(page_title="RISHU AI", page_icon="🤖")

# --- PASSWORD PROTECTION ---
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.title("🔒 RISHU ACCESS")
    pwd = st.text_input("Enter Access Code:", type="password")
    if st.button("Unlock"):
        if pwd == "76208":
            st.session_state.authenticated = True
            st.rerun()
        else:
            st.error("Access Denied.")
else:
    # --- RISHU INTERFACE ---
    st.title("🤖 RISHU")
    st.caption("Bold. Intelligent. Practical.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("State your query..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # RISHU'S PERSONALITY INSTRUCTIONS
        full_prompt = f"System: You are RISHU, a bold, intelligent AI assistant with a practical, masculine tone. Be direct and no-nonsense. User says: {prompt}"
        
        response = model.generate_content(full_prompt)
        
        with st.chat_message("assistant"):
            st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
        
      
