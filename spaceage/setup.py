import os
import dotenv


def setup():
    dotenv.load_dotenv()
    using_langsmith()


def using_langsmith():
    api_key = os.getenv('LANGCHAIN_API_KEY', None)
    if api_key is None:
        raise Exception('LANGCHAIN_API_KEY is not set')

    os.environ['LANGCHAIN_TRACING_V2'] = 'true'
    os.environ['LANGCHAIN_PROJECT'] = 'SpaceAge'
    os.environ['LANGCHAIN_ENDPOINT'] = 'https://api.smith.langchain.com'
    os.environ['LANGCHAIN_API_KEY'] = api_key
