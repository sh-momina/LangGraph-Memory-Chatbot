import streamlit as st
from chatBot_backend import workflow
from langchain_core.messages import HumanMessage
import uuid

# *****************************Utility Functions************************************

def generate_thread_id():
    
    thread_id = uuid.uuid4()
    return thread_id

def reset_chat():
    thread_id = generate_thread_id()
    st.session_state["thread_id"] = thread_id
    add_thread(st.session_state["thread_id"])
    st.session_state["message_history"] = []
    
def add_thread(thread_id):
    if thread_id not in st.session_state["thread_id_list"]:
        st.session_state["thread_id_list"].append(thread_id)
        
def load_conversation(thread_id):
    state = workflow.get_state(config={'configurable': {'thread_id': thread_id}})
    # Check if messages key exists in state values, return empty list if not
    return state.values.get('messages', [])

# *******************************Session State****************************************

# when every time press enter this complte code re run so message list empty .. 
# so in streamlit use " session state -> dict " .. which only refresh when u manually re run ...

if "message_history" not in st.session_state:
    st.session_state["message_history"] = []
    
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()
    
if "thread_id_list" not in st.session_state:
    st.session_state["thread_id_list"] = []

add_thread(st.session_state["thread_id"])

    
# ******************************Sidebar UI******************************************

st.sidebar.title("LangGrapg ChatBot")

if st.sidebar.button("Start New Chat"):
    reset_chat()

st.sidebar.header("My Conversations")

for i in st.session_state["thread_id_list"][::-1]:
    if st.sidebar.button(f"Conversation #id \n\n{str(i)}"):
        st.session_state["thread_id"] = i
        messages = load_conversation(i)
        
        temp_messages = []
        
        for message in messages:
            if isinstance(message, HumanMessage):
                role = "user"
            else:
                role = "assistant"
                
            temp_messages.append({"role" : role, "content" : message.content})
        st.session_state["message_history"] = temp_messages


# **************************************Main UI***********************************

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
    
    config = {"configurable" : {"thread_id" : st.session_state["thread_id"]}}

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