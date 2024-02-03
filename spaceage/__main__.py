import asyncio


if __name__ == "__main__":
    from spaceage.setup import setup
    from spaceage.app import testing_testing, agent_flow_test
    from spaceage.utils import ct, Colors

    setup()
    try:
        # asyncio.run(testing_testing())
        agent_flow_test()
    except KeyboardInterrupt:
        print(ct("<INTERRUPTED>\n\nGoodbye", Colors.RED))
