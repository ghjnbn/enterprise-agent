import json

from langchain_core.messages import HumanMessage, ToolMessage

from app.agent.llm import llm
from app.agent.state import AgentState
from app.agent.schema import TicketAnalysis
from app.agent.tools import check_service, restart_service


# 将工具提供给模型，使模型能够生成标准的工具调用请求。
tools = [check_service, restart_service]
llm_with_tools = llm.bind_tools(tools)


def llm_analyze_ticket(state: AgentState):
    """
    工单分析节点：
    使用大模型分析工单，并通过 JSON + Pydantic 验证决策。
    """

    prompt = f"""
你是企业 IT 运维 Agent。

你的任务是分析 IT 工单，并输出机器可执行的决策。

工单描述：
{state["description"]}

你必须严格返回 JSON 格式。

category 只能从以下类别选择一个：
- service_issue
- database_issue
- network_issue
- hardware_issue
- security_issue

action 只能从以下动作选择一个：
- restart_service
- check_service
- manual check

reason 用中文说明判断原因。

返回格式：
{{
    "category": "service_issue",
    "action": "check_service",
    "reason": "需要先检查服务状态"
}}
"""

    response = llm.invoke(prompt)

    data = json.loads(response.content)

    ticket_analysis = TicketAnalysis(**data)

    state["category"] = ticket_analysis.category
    state["action"] = ticket_analysis.action
    state["analysis"] = ticket_analysis.reason

    return state


def call_tool_agent(state: AgentState):
    """
    工具调用节点：
    根据工单分析结果，决定是否调用已注册工具。
    工具执行本身由 LangGraph ToolNode 负责。
    """

    messages = state.get("messages", [])
    is_first_call = not messages

    # 首次进入节点时，建立初始消息。
    if is_first_call:
        prompt = f"""
你是企业 IT 运维 Agent，现在需要根据已完成的工单分析来执行下一步。

工单编号：{state["ticket_id"]}
工单描述：{state["description"]}
故障类别：{state["category"]}
分析建议动作：{state["action"]}
分析理由：{state["analysis"]}

你可以使用以下工具：
1. check_service(service_name)：检查服务状态。
2. restart_service(service_name)：重启服务。

执行规则：
- 如果分析建议动作是 check_service，必须调用 check_service。
- 如果分析建议动作是 restart_service，必须调用 restart_service。
- 如果分析建议动作是 manual check，不要调用任何工具，应说明需要人工检查。
- 当前只是模拟运维环境。工单没有指定服务名称时，使用 nginx 作为测试对象。
- 调用工具时必须使用工具定义中的准确参数名称。
- 对于需要调用工具的情况，不要只用自然语言描述操作，必须发出工具调用。
"""

        messages = [HumanMessage(content=prompt)]

    # 如果上一轮调用了工具，工具结果已经在消息历史中。
    tool_messages = [
        message
        for message in messages
        if isinstance(message, ToolMessage)
    ]

    updates = {}

    if tool_messages:
        # 保存最近一次工具执行结果。
        updates["result"] = str(tool_messages[-1].content)

    # 模型只能提出工具调用请求，不会在这里直接执行 Python 工具函数。
    response = llm_with_tools.invoke(messages)

    if is_first_call:
        # 首次调用需要将用户消息和 AI 消息一起写入状态。
        updates["messages"] = messages + [response]
    else:
        # 后续调用只追加新产生的 AI 消息。
        updates["messages"] = [response]

    if not response.tool_calls and state["action"] == "manual check":
        updates["result"] = "need manual check"

    return updates
