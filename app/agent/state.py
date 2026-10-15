from typing import Annotated, TypedDict

from langgraph.graph.message import add_messages


class AgentState(TypedDict):

    ticket_id: str

    description: str

    category: str

    action: str

    result: str

    analysis: str

    messages: Annotated[list, add_messages]