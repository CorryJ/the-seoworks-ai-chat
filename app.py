from openai import OpenAI
import streamlit as st
import os
from streamlit.components.v1 import html

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
        "**Select a GPT model:**",
        ["gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"],
        index=0,
        horizontal=True,
    )
    st.divider()

with st.sidebar:
    use_instructions = st.radio(
        "**Do you want to use instuctions?**",
        ["Yes", "No"],
        index=0,
        horizontal=True,
        help = "Selecting yes will improve the quality of the response by adding further instruction to the commands \
            including using UK english and not using certin words to make the response sound less AI generated"
    )
    st.divider()

if st.sidebar.button("Clear Conversation"):
    st.session_state.messages = []


client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
# client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "openai_model" not in st.session_state:
    st.session_state["openai_model"] = "gpt-4o"

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"],avatar = "https://www.seoworks.co.uk/wp-content/themes/seoworks/assets/images/fav.png"):
        st.markdown(message["content"])

bannedWord1 = "Everest, Matterhorn, levate, juncture, moreover, landscape, utilise, maze, labyrinth, cusp, hurdles, bustling, harnessing, unveiling the power,\
       realm, depicted, demystify, insurmountable, new era, poised, unravel, entanglement, unprecedented, eerie connection, unliving, \
       beacon, unleash, delve, enrich, multifaceted, elevate, discover, supercharge, unlock, unleash, tailored, elegant, delve, dive, \
       ever-evolving, pride, realm,  meticulously, grappling, superior, weighing,  merely, picture, architect, adventure, journey, embark , \
       navigate, navigation, navigating, enchanting, world, dazzle, tapestry, in this blog, in this article, dive-in, in today's, right place, \
        let's get started, imagine this, picture this, consider this, just explored, tackle, delve"


instructions = "1. Write in UK English at all times e.g. (e.g., humanise instead of humanize, colour instead of color).  \
2. Avoid jargon and unnecessarily complex word choices. 4. Clarity is crucial. Do not use emojis or exclamation marks. 3. You MUST not include any of the following words in the response:  {0}".format(bannedWord1)


if prompt := st.chat_input("Add your prompt here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user", avatar="https://www.seoworks.co.uk/wp-content/themes/seoworks/assets/images/fav.png"):
        st.markdown(f"**{prompt}**")

    with st.chat_message("assistant", avatar="https://www.seoworks.co.uk/wp-content/themes/seoworks/assets/images/fav.png"):
        message_placeholder = st.empty()
        try:
            with st.spinner("Waiting for response..."):
                full_response = ""
                for response in client.chat.completions.create(
                    model=st.session_state["openai_model"],
                    messages=[
                        {"role": m["role"], "content": m["content"] + (instructions if use_instructions == "Yes" and m["role"] == "user" else "")}
                        for m in st.session_state.messages
                    ],
                    stream=True,
                ):
                    full_response += (response.choices[0].delta.content or "")
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            st.markdown(f"This response used the {model} model")
            st.markdown("Instructions used" if use_instructions == "Yes" else "Instructions not used")

        except Exception as e:
            st.error(f'An error occurred: {str(e)}')
            st.markdown('<div style="text-align: center; font-size:18px;">Apologies, an error occurred. Please try again later.</div>', unsafe_allow_html=True)