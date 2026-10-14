from typing import TypedDict


class AgentState(TypedDict):

    ticket_id: str

    description: str

    category: str

    action: str

    result: str


    analysis: str