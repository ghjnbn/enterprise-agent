from app.agent.graph import graph


if __name__ == "__main__":


    ticket = {

        "ticket_id": "INC001",

        "description": "服务器服务异常",

        "category": "",

        "action": "",

        "result": ""

    }


    result = graph.invoke(ticket)


    print(result)