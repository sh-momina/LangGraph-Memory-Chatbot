from langgraph.graph import START, END, StateGraph
from langchain_openai import ChatOpenAI
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage
from langgraph.graph.message import add_messages
from dotenv import load_dotenv
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import tool

import requests
import random

load_dotenv()
model = ChatOpenAI()

# using pre buitl tools
search_tool = DuckDuckGoSearchRun(region='us-en')

# making custom tools
@tool
def calculator(num1:float, num2:float, operator:str) -> dict:
    """
    perform the basic arthamatic operations on the two numbers.
    support the oprations: add, sun, mul, div
    """
    
    try:
        if operator == "add":
            result = num1 + num2
        elif operator == "sub":
            result = num1 - num2
        elif operator == "mul":
            result = num1 * num2
        elif operator == "div":
            if num2 == 0:
                return {"error" : "divided by zero"}
            result = num1 / num2
        else:
            return {"error" : f"unsupproted {operator}"}
        
        return {"first_num" : num1,"second_num" : num2,"operator" : operator,"result" : result}
    
    except Exception as e:
        return {"error" : str(e)}
    
    
@tool
def get_stock_price(symbol:str) -> dict:
    """
    fetch the latest stock price for a given symbol(e.g. 'AAPL', 'TSLA')
    using alpha vantage with api key in the url
    """
    
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey=A7WLETJFD8MVT82B'
    r = requests.get(url)
    data = r.json()
    
    return data

tools = [search_tool, get_stock_price, calculator]

model_with_tools = model.bind_tools(tools)

class ChatState(TypedDict):
    messages : Annotated[list[BaseMessage], add_messages]

def chat_node(state:ChatState):
    """The model(llm) may answer or request a tool call"""
    messages = state["messages"]
    responce = model_with_tools.invoke(messages)
    return {"messages" : [responce]}

tool_node = ToolNode(tools)

    
graph = StateGraph(ChatState)
graph.add_node("chat_node", chat_node)
graph.add_node("tools", tool_node)

graph.add_edge(START, "chat_node")
graph.add_conditional_edges("chat_node", tools_condition)
graph.add_edge("tools", "chat_node")

workflow = graph.compile()


while True:
    
    question = input("You : ")
    if question == "exit":
        break
    answer = workflow.invoke(
        {
            "messages" : HumanMessage(content=question)
        }
    )
    
    print("AI : ", answer["messages"][-1].content)
