import enquiries
import asyncio

from spaceage.runnables import ollama_mistral, openai_one_tool


# enum class with menu choices
class MenuChoices:
    OLLAMA_MISTRAL = "Ollama: Mistral"
    OPENAI_ONE_TOOL = "OpenAI: 1 tool"
    QUIT = "quit"




def menu():
    running = True

    while running:
        # choice = enquiries.choose(ct("Choose a test to run", Colors.YELLOW), ["testing_testing", "agent_flow_test", "quit"])
        choice = enquiries.choose(ct("Choose a test to run", Colors.YELLOW), [MenuChoices.OLLAMA_MISTRAL, MenuChoices.OPENAI_ONE_TOOL, MenuChoices.QUIT])
        if choice == MenuChoices.OLLAMA_MISTRAL:
            asyncio.run(ollama_mistral())
        elif choice == MenuChoices.OPENAI_ONE_TOOL:
            openai_one_tool()
        elif choice == MenuChoices.QUIT:
            running = False




if __name__ == "__main__":
    from spaceage.setup import setup
    from spaceage.utils import ct, Colors

    setup()

    try:
        menu()
    except KeyboardInterrupt:
        print(ct("<INTERRUPTED>\n\nGoodbye", Colors.RED))
    except enquiries.error.SelectionAborted:
        print(ct("\n<FORCE QUIT>\n\nGoodbye", Colors.YELLOW))
