from app.agent.state import AgentState

from app.agent.tools import restart_service


def analyze_ticket(state: AgentState):

    """
    工单分析节点
    """

    description = state["description"]


    if "服务" in description:

        state["category"] = "service_issue"

        state["action"] = "restart_service"


    return state



def execute_action(state: AgentState):

    """
    工具执行节点
    """


    if state["action"] == "restart_service":

        result = restart_service(
            "nginx"
        )

        state["result"] = str(result)


    return state