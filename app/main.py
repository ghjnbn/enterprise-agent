from langchain_core.messages import HumanMessage

from app.agent.graph import graph


def main():

    result = graph.invoke(
        {
            "messages": [
                HumanMessage(
                    content="北京天气怎么样？"
                )
            ]
        }
    )


    print(
        result["messages"][-1].content
    )


if __name__ == "__main__":

    main()