from typing import TypedDict


class AgentState(TypedDict):
    """
    Agent运行状态
    """

    ticket_id: str

    description: str

    category: str

    action: str

    result: str