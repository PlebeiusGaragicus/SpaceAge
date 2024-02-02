# from langchain.llms import ollama
from langchain_community.llms import ollama
from langchain_community.tools import DuckDuckGoSearchRun

from spaceage.utils import ct, Colors

# PROMPT = """
# Was the washing machine or the incandescant light bulb a more life-changing invention?
# """

async def runflow():
    search_tool = DuckDuckGoSearchRun()
    mistral_ollama = ollama.Ollama(model='mistral')

    # prompt = input("Enter a prompt: ")
    prompt = input(ct("\nEnter a prompt: ", Colors.YELLOW))

    async for t in mistral_ollama.astream(input=prompt):
        print(ct(t, Colors.BLUE), end='', flush=True)
