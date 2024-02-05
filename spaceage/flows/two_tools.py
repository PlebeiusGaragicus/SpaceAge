import os
import operator
from typing import TypedDict, Annotated, List, Union

from langchain import hub
from langchain.agents import create_openai_functions_agent, create_openai_tools_agent

from langchain_openai.chat_models import ChatOpenAI
from langchain_community.llms.ollama import Ollama, OllamaEndpointNotFoundError
from langchain_experimental.llms.ollama_functions import OllamaFunctions

from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.agents import AgentAction, AgentFinish
from langchain_core.messages import BaseMessage
from langchain_core.agents import AgentFinish
from langgraph.prebuilt.tool_executor import ToolExecutor
from langgraph.graph import END, StateGraph



from spaceage.utils import Colors, color_print




class AgentState(TypedDict):
   # The input string
   input: str


   # The list of previous messages in the conversation
   chat_history: list[BaseMessage]


   # The outcome of a given call to the agent
   # Needs `None` as a valid type, since this is what this will start as
   agent_outcome: Union[AgentAction, AgentFinish, None]


   # List of actions and corresponding observations
   # Here we annotate this with `operator.add` to indicate that operations to
   # this state should be ADDED to the existing values (not overwrite it)
   intermediate_steps: Annotated[list[tuple[AgentAction, str]], operator.add]







def create_tavily_runnable():
    if os.environ["TAVILY_API_KEY"] is None:
        raise ValueError("Tavily API Key not found")


    ### CREATE THE AGENT
    tools = [TavilySearchResults(max_results=5)]

    # Get the prompt to use - you can modify this!
    prompt = hub.pull("hwchase17/openai-functions-agent")
    # color_print(f"using prompt: {prompt}", Colors.YELLOW)
    """
    input_variables=['agent_scratchpad', 'input']
    input_types={
        'chat_history': typing.List[
            typing.Union[
                langchain_core.messages.ai.AIMessage,
                langchain_core.messages.human.HumanMessage,
                langchain_core.messages.chat.ChatMessage,
                langchain_core.messages.system.SystemMessage,
                langchain_core.messages.function.FunctionMessage,
                langchain_core.messages.tool.ToolMessage
                ]
            ],
        'agent_scratchpad': typing.List[
            typing.Union[
                langchain_core.messages.ai.AIMessage,
                langchain_core.messages.human.HumanMessage,
                langchain_core.messages.chat.ChatMessage,
                langchain_core.messages.system.SystemMessage,
                langchain_core.messages.function.FunctionMessage,
                langchain_core.messages.tool.ToolMessage
                ]
            ]
    }
    messages=[
        SystemMessagePromptTemplate(
            prompt=PromptTemplate(
                input_variables=[],
                template='You are a helpful assistant')),
                MessagesPlaceholder(
                    variable_name='chat_history',
                    optional=True),
                HumanMessagePromptTemplate(
                    prompt=PromptTemplate(
                        input_variables=['input'],
                        template='{input}'
                        )
                    ),
                MessagesPlaceholder(
                    variable_name='agent_scratchpad'
                )
    ]
    """

    # Choose the LLM that will drive the agent
    llm = ChatOpenAI(model="gpt-3.5-turbo-1106", streaming=True)
    # model_name = 'llama2'
    # llm = OllamaFunctions(model="llama2", streaming=True)
    # model_name = 'mistralai/Mixtral-8x7B-Instruct-v0.1'

    # try:
        # llm = Ollama(model=model_name)
    # except OllamaEndpointNotFoundError:
    #     import ollama
    #     ollama.pull(model_name)
    #     llm = Ollama(model=model_name)


    # Construct the OpenAI Functions agent
    agent_runnable = create_openai_functions_agent(llm, tools, prompt)
    # agent_runnable = create_openai_tools_agent(llm, tools, prompt)



    # This a helper class we have that is useful for running tools
    # It takes in an agent action and calls that tool and returns the result
    tool_executor = ToolExecutor(tools)

    # Define the agent
    def run_agent(data):
        agent_outcome = agent_runnable.invoke(data)
        return {"agent_outcome": agent_outcome}

    # Define the function to execute tools
    def execute_tools(data):
        # Get the most recent agent_outcome - this is the key added in the `agent` above
        agent_action = data['agent_outcome']
        output = tool_executor.invoke(agent_action)
        return {"intermediate_steps": [(agent_action, str(output))]}

    # Define logic that will be used to determine which conditional edge to go down
    def should_continue(data):
        # If the agent outcome is an AgentFinish, then we return `exit` string
        # This will be used when setting up the graph to define the flow
        if isinstance(data['agent_outcome'], AgentFinish):
            return "end"
        # Otherwise, an AgentAction is returned
        # Here we return `continue` string
        # This will be used when setting up the graph to define the flow
        else:
            return "continue"





    # Define a new graph
    workflow = StateGraph(AgentState)

    # Define the two nodes we will cycle between
    workflow.add_node("agent", run_agent)
    workflow.add_node("action", execute_tools)

    # Set the entrypoint as `agent`
    # This means that this node is the first one called
    workflow.set_entry_point("agent")

    # We now add a conditional edge
    workflow.add_conditional_edges(
        # First, we define the start node. We use `agent`.
        # This means these are the edges taken after the `agent` node is called.
        "agent",
        # Next, we pass in the function that will determine which node is called next.
        should_continue,
        # Finally we pass in a mapping.
        # The keys are strings, and the values are other nodes.
        # END is a special node marking that the graph should finish.
        # What will happen is we will call `should_continue`, and then the output of that
        # will be matched against the keys in this mapping.
        # Based on which one it matches, that node will then be called.
        {
            # If `tools`, then we call the tool node.
            "continue": "action",
            # Otherwise we finish.
            "end": END
        }
    )

    # We now add a normal edge from `tools` to `agent`.
    # This means that after `tools` is called, `agent` node is called next.
    workflow.add_edge('action', 'agent')

    app = workflow.compile() # This compiles it into a LangChain Runnable,

    return app
