from openai import OpenAI
import streamlit as st
import os

###LIVE VERSION
# Setting page title and header
st.set_page_config(page_title="The SEO Works AI Bot", 
                   page_icon="https://www.seoworks.co.uk/wp-content/themes/seoworks/assets/images/fav.png", 
                   layout="wide",initial_sidebar_state="expanded")

#Defines custom css file
with open( "resources/style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)
file_name="resources/style.css"

# custom styling to remove red bar at top
st.markdown("""
<style>
	[data-testid="stDecoration"] {
		display: none;
	}
</style>
                
            """, unsafe_allow_html=True)

# Remove whitespace from the top of the page and sidebar
st.markdown("""
        <style>
               .block-container {
                    padding-top: 0rem;
                    padding-bottom: 0rem;
                    padding-left: 5rem;
                    padding-right: 5rem;
                }
        </style>
        """, unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.header("")
   
with col2:
    st.header("")
    st.image("resources/SeoWorksLogo-Dark.png")

with col3:
    st.header("")


st.markdown('<div style="text-align: center; font-size:24px;"><strong>The SEO Works AI Bot<strong></div>', unsafe_allow_html=True)

with st.sidebar:
    model = st.radio(
        "Select a GPT model",
        ["gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"],
        index=0,
        horizontal=True
    )

if st.sidebar.button("Clear Conversation"):
    st.session_state.messages = []

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = model

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar = "https://www.seoworks.co.uk/wp-content/themes/seoworks/assets/images/fav.png"):
        st.markdown(message["content"])

        # Add a button to copy text to clipboard after each message
        copy_text = message["content"]
        copy_button_code = f"""
            <button onclick="navigator.clipboard.writeText(`{copy_text}`)" style="padding: 5px 10px; margin-top: 10px;">
                Copy Response
            </button>
        """
        st.markdown(copy_button_code, unsafe_allow_html=True)

if prompt := st.chat_input("Add your prompt here..."):
    try:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar = "https://www.seoworks.co.uk/wp-content/themes/seoworks/assets/images/fav.png"):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar = "https://www.seoworks.co.uk/wp-content/themes/seoworks/assets/images/fav.png"):
            message_placeholder = st.empty()
            full_response = ""
            for response in client.chat.completions.create(
                model=st.session_state["openai_model"],
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ],
                stream=True,
            ):
                full_response += (response.choices[0].delta.content or "")
                message_placeholder.markdown(full_response + "▌")
            message_placeholder.markdown(full_response)
        
        st.session_state.messages.append({"role": "assistant", "content": full_response})

        # Add a button to copy the assistant's response
        copy_text = full_response
        copy_button_code = f"""
            <button onclick="navigator.clipboard.writeText(`{copy_text}`)" style="padding: 5px 10px; margin-top: 10px;">
                Copy Response
            </button>
        """
        st.markdown(copy_button_code, unsafe_allow_html=True)

    except:
        st.markdown('<div style="text-align: center; font-size:18px;">Apologies, the API is overloaded. Please call back later.</div>', unsafe_allow_html=True)
        