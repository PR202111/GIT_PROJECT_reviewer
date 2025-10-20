# main.py
import os

from documents_to_database import make_vector_store
from load_repo import SetUpRepo

def main():
    print("Menu\n1. for repo link\n2. local path")
    while(1):
        choice = (input("Enter your choice: ")).strip()
        link_path = (input("Enter the link or local path: ")).strip()

        if(choice == "1"):
            repo = SetUpRepo(link=link_path,path=None)
        elif choice == "2":
            repo = SetUpRepo(link=None,path=link_path)
        else:
             print("Wrong choice enter again")
             continue
        if repo == "reload_and_continue":
            continue
        else:
            print("repo initialised Successfully!!")
            break
    
    print("\nInitializing the Code Reviewer Agent\n")


    llm_chain, tools = create_reviewer_agent()
    print("Welcome to the Code Reviewer Agent (Ollama)!")
    print("Type your query (e.g., 'Show me main.py code') or 'exit' to quit.\n")

    while True:
        query = input("Your query: ")
        if query.lower() in ["exit", "quit"]:
            break

        # Execute tool first to fetch code from repo
        tool_output = tools[0].run(query)

        # Feed tool output to LLM for final answer
        response = llm_chain.run(input=query + "\n\nRepository info:\n" + tool_output)

        print("\n=== Agent Response ===")
        print(response)
        print("====================\n")

if __name__ == "__main__":
    main()
