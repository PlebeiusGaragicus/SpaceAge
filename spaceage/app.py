# from langchain.llms import ollama
from langchain_community.llms import ollama
from langchain_community.tools import DuckDuckGoSearchRun

from spaceage.utils import Colors, ct, print_color


async def testing_testing():
    search_tool = DuckDuckGoSearchRun()
    mistral_ollama = ollama.Ollama(model='mistral')

    # Was the washing machine or the incandescant light bulb a more life-changing invention?
    prompt = input(ct("\nEnter a prompt: ", Colors.YELLOW))

    async for t in mistral_ollama.astream(input=prompt):
        print_color(t, Colors.BLUE)




def agent_flow_test():
    from spaceage.flows.agent_exec import app
    user_prompt = input("What do you want to learn?  ")

    # inputs = {"input": "what is the weather in sf", "chat_history": []}
    inputs = {"input": user_prompt, "chat_history": []}
    for s in app.stream(inputs):
        print(list(s.values())[0])
        print("----")
