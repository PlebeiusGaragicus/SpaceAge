import asyncio


if __name__ == "__main__":
    from spaceage.setup import setup
    from spaceage.flow import runflow
    from spaceage.utils import ct, Colors

    setup()
    try:
        asyncio.run(runflow())
    except KeyboardInterrupt:
        print(ct("<INTERRUPTED>\n\nGoodbye", Colors.RED))
