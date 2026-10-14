import json

from app.agent.llm import llm

from app.agent.state import AgentState

from app.agent.schema import TicketAnalysis

from app.agent.tools import (
    restart_service,
    check_service
)



def llm_analyze_ticket(state):

    prompt = f"""
你是企业IT运维Agent。

你的任务是分析IT工单，并输出机器可执行的决策。


工单：

{state["description"]}


你必须严格返回JSON格式。

字段说明：

category:
只能从以下类别选择一个：

- service_issue
- database_issue
- network_issue
- hardware_issue
- security_issue


action:
只能从以下动作选择一个：

- restart_service
- check_service
- manual check


reason:
说明判断原因。


返回格式：

{{
    "category": "service_issue",
    "action": "check_service",
    "reason": "xxx"
}}
"""


    response = llm.invoke(prompt)


    data = json.loads(response.content)


    ticket_analysis = TicketAnalysis(
        **data
    )


    state["category"] = ticket_analysis.category

    state["action"] = ticket_analysis.action

    state["analysis"] = ticket_analysis.reason


    return state

def execute_action(state: AgentState):

    """
    工具执行节点
    """


    if state["action"] == "restart_service":

        result = restart_service(
            "nginx"
        )


    elif state["action"] == "check_service":

        result = check_service(
            "nginx"
        )


    else:

        result = {
            "message":"need manual check"
        }


    state["result"] = str(result)

    return state