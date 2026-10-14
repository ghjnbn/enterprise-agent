from app.agent.llm import llm

from app.agent.state import AgentState

from app.agent.tools import restart_service



def llm_analyze_ticket(
        state: AgentState
):


    prompt = f"""
你是企业IT运维专家。

分析下面工单：

{state["description"]}


输出：

问题类型

处理建议
"""


    response = llm.invoke(prompt)


    state["analysis"] = response.content


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