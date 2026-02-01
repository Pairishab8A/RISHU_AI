import streamlit as st
import google.generativeai as genai

# --- CONFIGURATION ---
# We will add your API key here in the next step
st.set_page_config(page_title="RISHU AI", page_icon="🤖")

# --- PASSWORD PROTECTION ---
def check_password():
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
                st.error("Access Denied. Incorrect Code.")
        return False
    return True

if check_password():
    # --- RISHU PERSONA ---
    st.title("🤖 RISHU")
    st.markdown("---")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("State your query..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # AI Response logic will be connected here
        response = f"RISHU: I am currently being initialized. I've received: '{prompt}'. Once you add the API Key, I will be fully functional."
        
        with st.chat_message("assistant"):
            st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
