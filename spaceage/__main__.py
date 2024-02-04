import enquiries
import asyncio

def menu():
    running = True
    while running:
        choice = enquiries.choose(ct("Choose a test to run", Colors.YELLOW), ["testing_testing", "agent_flow_test", "quit"])
        if choice == "testing_testing":
            # testing_testing()
            asyncio.run(testing_testing())
        elif choice == "agent_flow_test":
            agent_flow_test()
        elif choice == "quit":
            running = False
        # else:
        #     print("Invalid choice")
        #     menu()





if __name__ == "__main__":
    from spaceage.setup import setup
    from spaceage.app import testing_testing, agent_flow_test
    from spaceage.utils import ct, Colors

    setup()

    # choice = enquiries.choose("Choose a test to run", ["testing_testing", "agent_flow_test", "quit"])
    try:
        menu()
        # agent_flow_test()
    # except Exception as e:
        # print(e)
        # print(ct(f"An error occurred: {e}", Colors.RED))
    except KeyboardInterrupt:
        print(ct("<INTERRUPTED>\n\nGoodbye", Colors.RED))
    except enquiries.error.SelectionAborted:
        print(ct("\n<FORCE QUIT>\n\nGoodbye", Colors.YELLOW))
