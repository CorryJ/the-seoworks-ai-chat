from openai import OpenAI
import streamlit as st
import os

###LIVE VERSION
# Setting page title and header
st.set_page_config(page_title="The SEO Works AI Bot", 
                   page_icon="https://www.seoworks.co.uk/wp-content/themes/seoworks/assets/images/fav.png", 
                   layout="centered",initial_sidebar_state="collapsed")

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
# st.markdown('<div style="text-align: center; font-size:22px;">Use this app to access the best gpt model</div>', unsafe_allow_html=True)

# Spacers for layout purposes
# st.write("#")

# st.markdown(
#         """
#         <style>
#         .stMarkdownContainer p {
#             font-size: 20px;
#         }
#         </style>
#         """,
#         unsafe_allow_html=True,
#     )

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4-turbo"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"],avatar = "https://www.seoworks.co.uk/wp-content/themes/seoworks/assets/images/fav.png"):
        st.markdown(message["content"])


if prompt := st.chat_input("Add you prompt here..."):
    try:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user",avatar = "https://www.seoworks.co.uk/wp-content/themes/seoworks/assets/images/fav.png" ):
            st.markdown(prompt)

        with st.chat_message("assistant", avatar = "https://www.seoworks.co.uk/wp-content/themes/seoworks/assets/images/fav.png" ):
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
    except:
        st.markdown('<div style="text-align: center; font-size:18px;">Apologies, the API is overloaded. Please call back later.</div>', unsafe_allow_html=True)

