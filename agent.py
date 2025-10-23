from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import START, StateGraph, MessagesState
from langgraph.prebuilt import tools_condition, ToolNode
from tools_loader import create_tool_list  
from CONFIG import REPO_PATH,MODEL

def summarize_tool_output(tool_call_result):
    """
    If the LLM decided to call a tool, run the tool and summarize it for the user.
    """
    if isinstance(tool_call_result, dict) and "name" in tool_call_result:
        # run the tool
        tool_name = tool_call_result["name"]
        params = tool_call_result.get("parameters", {})
        tool = next(t for t in tools if t.name == tool_name)
        output = tool.run(**params)
        
        # summarize with LLM
        summary_prompt = [
            sys_msg,
            HumanMessage(content=f"Summarize this tool output for the user:\n{output}")
        ]
        return llm.invoke(summary_prompt).content
    return tool_call_result


llm = ChatOllama(model=MODEL)  


tools = create_tool_list()


llm_with_tools = llm.bind_tools(tools)


sys_msg = SystemMessage(
    content=(
        f"You are a helpful coding assistant with access to tools "
        f"that help analyze GitHub projects located at path {REPO_PATH} and repositories. "
        "At end of outputs also give the tools and arguments used for answering"
    )

)


def reasoner(state: MessagesState):
    return {
        "messages": [
            llm_with_tools.invoke([sys_msg] + state["messages"])
        ]
    }


builder = StateGraph(MessagesState)
builder.add_node("reasoner", reasoner)
builder.add_node("tools", ToolNode(tools))

builder.add_edge(START, "reasoner")
builder.add_conditional_edges("reasoner", tools_condition)
builder.add_edge("tools", "reasoner")

react_graph = builder.compile()


if __name__ == "__main__":
    print("GitHub Project Analyzer (type 'exit' or 'quit' to stop)\n")
    conversation = []  # keep message history

    while True:
        user_input = input("You: ")
        if user_input.lower() in {"exit", "quit"}:
            print("Goodbye 👋")
            break

        
        conversation.append(HumanMessage(content=user_input))

        
        result = react_graph.invoke({"messages": conversation})

        
        last_message = result["messages"][-1]
        print(f"Agent: {last_message.content}\n")

        
        conversation = result["messages"]
