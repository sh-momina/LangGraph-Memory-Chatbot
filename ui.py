import streamlit as st
from chatBot_backend import llm_call

# when every time press enter this complte code re run so message list empty .. 
# so in streamlit use " session state -> dict " .. which only refresh when u manually re run ...

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []


for i in st.session_state["message_history"]:
    with st.chat_message(i["role"]):
        st.text(i["content"])

user_input = st.chat_input("Type here ... ")


if user_input:
    
    st.session_state["message_history"].append(
        {
            "role" : "user",
            "content" : user_input
        }
    )
    with st.chat_message("user"):
        st.text(user_input)
        
    st.session_state["message_history"].append(
        {
            "role" : "assistant",
            "content" : user_input
        }
    )
    with st.chat_message("assistant"):
        ai_response = llm_call(user_input)
        st.text(ai_response)