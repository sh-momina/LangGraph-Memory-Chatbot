import streamlit as st
from chatBot_backend import workflow
from langchain_core.messages import HumanMessage

thread_id = "1"
config = {"configurable" : {"thread_id" : thread_id}}

# when every time press enter this complte code re run so message list empty .. 
# so in streamlit use " session state -> dict " .. which only refresh when u manually re run ...

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []


for i in st.session_state["message_history"]:
    with st.chat_message(i["role"]):
        st.text(i["content"])

query = st.chat_input("Type here ... ")


if query:
    
    st.session_state["message_history"].append(
        {
            "role" : "user",
            "content" : query
        }
    )
    with st.chat_message("user"):
        st.text(query)
        
        
    with st.chat_message("assistant"):
        ai_response = st.write_stream(
            message_chunk.content
            for message_chunk, metadata in workflow.stream(
                {"messages": HumanMessage(content=query)},
                config=config,
                stream_mode="messages"
            )
        )
     
    st.session_state["message_history"].append(
        {
            "role" : "assistant",
            "content" : ai_response
        }
    )