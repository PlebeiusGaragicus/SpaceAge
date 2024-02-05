import json
from langchain_community.llms import ollama

from spaceage.utils import Colors, ct, print_tokens_in_color


async def ollama_mistral():
    mistral_ollama = ollama.Ollama(model='mistral')

    # Was the washing machine or the incandescant light bulb a more life-changing invention?
    prompt = input(ct("\nEnter a prompt: ", Colors.YELLOW))

    async for t in mistral_ollama.astream(input=prompt):
        print_tokens_in_color(t, Colors.BLUE)




def openai_one_tool():
    from spaceage.flows.single_tool import create_tavily_runnable, AgentState
    from langchain_core.agents import AgentFinish, AgentActionMessageLog

    app = create_tavily_runnable()

    user_prompt = input(ct("What do you want to learn?  ", Colors.CYAN))
    inputs = {"input": user_prompt, "chat_history": []}

    # stream the steps, not the tokens ;)
    for s in app.stream(inputs):

        ### THE AGENT HAS FINISHED! ###
        first_key = list(s.keys())[0]
        if first_key == '__end__':
            print(ct("\n---\nAnswer:", Colors.BLUE))

            result = s['__end__']["agent_outcome"].return_values['output']
            print( ct(result, Colors.GREEN) )

        if first_key == 'agent':
            result = s['agent']['agent_outcome']

            if isinstance(result, AgentActionMessageLog):
                print(f"{ct('AGENT CALLING TOOL: ', Colors.MAGENTA)}{ct(f'{result.tool}', Colors.RED)}")

            # AGENT THINKS IT'S DONE
            # if isinstance(result, AgentFinish):
            #     print(ct("AGENT THINKS IT'S DONE!!", Colors.MAGENTA))


        if first_key == 'action':
            # actions = result = s['action']['intermediate_steps']
            print(ct("REVIEWING TOOL RESULTS...", Colors.MAGENTA))
