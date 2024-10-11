from openai import OpenAI
import streamlit as st
import os
from streamlit.components.v1 import html



# Setting page config and styling (unchanged)
st.set_page_config(page_title="The SEO Works AI Bot", 
                   page_icon="https://www.seoworks.co.uk/wp-content/themes/seoworks/assets/images/fav.png", 
                   layout="wide", initial_sidebar_state="collapsed")


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




# Initialize session state variables
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "gpt-4o"

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "clear_flag" not in st.session_state:
    st.session_state.clear_flag = False

if "txt_to_analyse_1" not in st.session_state:
    st.session_state.txt_to_analyse_1 = ""

if "txt_to_analyse_2" not in st.session_state:
    st.session_state.txt_to_analyse_2 = ""

if "txt_to_analyse_3" not in st.session_state:
    st.session_state.txt_to_analyse_3 = ""

# Function to clear conversation, set clear flag, and clear input areas
def clear_conversation():
    st.session_state.chat_history = []
    st.session_state.clear_flag = True
    st.session_state.txt_to_analyse_1 = ""
    st.session_state.txt_to_analyse_2 = ""
    st.session_state.txt_to_analyse_3 = ""

# Sidebar options
with st.sidebar:
    st.header("Options")
    
    model = st.radio(
        "**Select a GPT model:**",
        ["gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"],
        index=0,
        horizontal=True,
    )
    
    use_instructions = st.radio(
        "**Do you want to use instructions?**",
        ["Yes", "No"],
        index=0,
        horizontal=True,
        help="Selecting yes will improve the quality of the response by adding further instruction to the commands "
             "including using UK English and not using certain words to make the response sound less AI generated"
    )
    
    if st.button("Clear Conversation"):
        clear_conversation()

# Text areas for TOV sample analysis
txt_to_analyse_1 = st.text_area(label="**TOV sample text to analyse 1**", value=st.session_state.txt_to_analyse_1, placeholder="Add sample of client text here", key="tov1")
txt_to_analyse_2 = st.text_area(label="**TOV sample text to analyse 2**", value=st.session_state.txt_to_analyse_2, placeholder="Add sample of client text here", key="tov2")
txt_to_analyse_3 = st.text_area(label="**TOV sample text to analyse 3**", value=st.session_state.txt_to_analyse_3, placeholder="Add sample of client text here", key="tov3")

# Update session state with current text area values
st.session_state.txt_to_analyse_1 = txt_to_analyse_1
st.session_state.txt_to_analyse_2 = txt_to_analyse_2
st.session_state.txt_to_analyse_3 = txt_to_analyse_3

# Initialize OpenAI client
client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])

# Display chat history
for message in st.session_state.chat_history:
    with st.chat_message(message["role"], avatar="https://www.seoworks.co.uk/wp-content/themes/seoworks/assets/images/fav.png"):
        st.markdown(message["content"])

# Banned words and instructions
bannedWord1 = "Everest, Matterhorn, levate, juncture, moreover, landscape, utilise, maze, labyrinth, cusp, hurdles, bustling, harnessing, unveiling the power, realm, depicted, demystify, insurmountable, new era, poised, unravel, entanglement, unprecedented, eerie connection, unliving, beacon, unleash, delve, enrich, multifaceted, elevate, discover, supercharge, unlock, unleash, tailored, elegant, delve, dive, ever-evolving, pride, realm,  meticulously, grappling, superior, weighing,  merely, picture, architect, adventure, journey, embark , navigate, navigation, navigating, enchanting, world, dazzle, tapestry, in this blog, in this article, dive-in, in today's, right place, let's get started, imagine this, picture this, consider this, just explored, tackle, delve"

TOV_instructions = f"Analyse the style of writing used in the text here: {txt_to_analyse_1} and here {txt_to_analyse_2} and here {txt_to_analyse_3} and use this style in the output you create. Write in UK English at all times e.g. (e.g., humanise instead of humanize, colour instead of color). Avoid jargon and unnecessarily complex word choices. Clarity is crucial. Do not use emojis or exclamation marks. You MUST not include any of the following words in the response: {bannedWord1}"

# Chat input and response
if user_input := st.chat_input("Add your prompt here..."):
    st.session_state.chat_history.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="https://www.seoworks.co.uk/wp-content/themes/seoworks/assets/images/fav.png"):
        st.markdown(f"**{user_input}**")

    with st.chat_message("assistant", avatar="https://www.seoworks.co.uk/wp-content/themes/seoworks/assets/images/fav.png"):
        message_placeholder = st.empty()
        try:
            with st.spinner("Waiting for response..."):
                full_response = ""
                for response in client.chat.completions.create(
                    model=st.session_state.selected_model,
                    messages=[
                        {"role": m["role"], "content": m["content"] + (TOV_instructions if use_instructions == "Yes" and m["role"] == "user" else "")}
                        for m in st.session_state.chat_history
                    ],
                    stream=True,
                ):
                    full_response += (response.choices[0].delta.content or "")
                    message_placeholder.markdown(full_response + "▌")
                message_placeholder.markdown(full_response)
            
            word_count = len(full_response.split())
            st.session_state.chat_history.append({"role": "assistant", "content": full_response})
            st.markdown(f"This response used the {model} model")
            st.markdown(f"Word count: {word_count}")
            st.markdown("Template instructions used" if use_instructions == "Yes" else "Template instructions not used")

        except Exception as e:
            st.error(f'An error occurred: {str(e)}')
            st.markdown('<div style="text-align: center; font-size:18px;">Apologies, an error occurred. Please try again later.</div>', unsafe_allow_html=True)