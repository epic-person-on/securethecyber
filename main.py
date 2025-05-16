import os
from langchain.agents import Tool, AgentExecutor, create_react_agent
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
from tools.tools import *
from dotenv import load_dotenv

load_dotenv()

shell = bash

tools = [
    Tool(
        name="Shell",
        func=shell.run,
        description="Useful for running bash commands requires you to use absolute directories and can't change directory."
    ),
    Tool(
        name="Clamscan",
        func=clamav.run,
        description="Useful for running anti virus scans on a directory. You only need to run this once!"
    )
]

llm = ChatGroq(
    temperature=0.7,
    model="llama3-8b-8192",
    api_key=os.getenv("Groq_API_KEY"),
)

template = """Answer the following questions as best you can. You have access to the following tools:

{tools}

Use the following format:

Question: the input question you must answer
Thought: you should always think about what to do
Action: the action to take, should be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (this Thought/Action/Action Input/Observation can repeat N times)
Thought: I now know the final answer
Final Answer: the final answer to the original input question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""


agent = create_react_agent(
    llm=llm,
    tools=tools,
    prompt=PromptTemplate.from_template(template)
)

agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True,
    memory=ConversationBufferMemory(memory_key="chat_history")
)

def ask_question(query):
    """
    Function to ask a question to the agent and get a response
    """
    try:
        response = agent_executor.invoke({"input": query})
        return response.get("output", "Sorry, I couldn't generate a response.")
    except Exception as e:
        return f"An error occurred: {str(e)}"


def main():
    print(ask_question("scan the ./ directory for viruses"))


if __name__ == "__main__":
    main()
