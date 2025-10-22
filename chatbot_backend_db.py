from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI
from typing import Annotated, TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, HumanMessage
from dotenv import load_dotenv
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

load_dotenv()
model = ChatOpenAI(model="gpt-4o")

class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages]
    
def chat_node(state : ChatState):
    messages = state["messages"]
    result = model.invoke(messages)
    return {"messages" : [result]}

# only used in single thread so check same thread false so it dont check and give errors coz we are changing multiple threads 
connection = sqlite3.connect(database="langGraph_chatbot_db", check_same_thread=False)
checkpointer = SqliteSaver(conn=connection)

graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

workflow = graph.compile(checkpointer=checkpointer)

# like each person intracting have their own thread id, so bot can config who is taking now 
# like for momina thread id -> 1

# thread_id = "1"
# config = {"configurable" : {"thread_id" : thread_id}}

# def llm_call(query : str):
    
#     result = workflow.invoke({
#         "messages": HumanMessage(content=query)
#     }, config=config)

#     ai_reply = result["messages"][-1].content
#     return ai_reply

# result = workflow.get_state(config=config)
# print(result)

# result = llm_call("whats my name?")
# print(result)

def extract_unique_thread_ids():
    all_threads = set()
    for cp in checkpointer.list(None):
        all_threads.add(cp.config["configurable"]["thread_id"])

    # print(list(all_threads)) 
    return list(all_threads)
    
