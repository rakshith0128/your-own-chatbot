from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import(
    SystemMessage,
    HumanMessage,
    AIMessage
)
import streamlit as st
from streamlit_chat import message

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv(),override=True)

st.set_page_config(
    page_title= "Your Custom Assistant",
    page_icon = '🤖'
)

st.subheader("Your custom chat bot 🤖")
chat = ChatGoogleGenerativeAI(model="gemini-1.5-pro", temperature=0.5)

if 'messages' not in st.session_state:
    st.session_state.messages =[]

with st.sidebar:
    system_message = st.text_input(label ='System role (optional)')
    user_prompt = st.text_input(label = 'send a message')
    if system_message:
        if not any(isinstance(x,SystemMessage) for x in st.session_state.messages):
            st.session_state.messages.append(
                SystemMessage(content = system_message)
            )

        
    if user_prompt:
        st.session_state.messages.append(
        HumanMessage(content = user_prompt)
      )  

        with st.spinner("working on your request..."):
            response = chat(st.session_state.messages)

        st.session_state.messages.append(AIMessage(content = response.content))


# message('this is a custom llm',is_user=False )
# message('this is the user',is_user=True )

if len(st.session_state.messages) >= 1:
    if not isinstance(st.session_state.messages[0], SystemMessage):
        st.session_state.messages.insert(0, SystemMessage(content ='''You are a helpful assistant who remembers the user's previous messages during this session. 
        Use earlier messages as context to answer current questions accurately.
        '''))


for i,msg in enumerate(st.session_state.messages[1:]):
    if i%2 == 0:
        message(msg.content, is_user=True , key= f'{i} +  🤙')
    else:
        message(msg.content, is_user=False,key =f'{i} + 🤖')
