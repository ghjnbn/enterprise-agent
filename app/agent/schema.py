from pydantic import BaseModel


class TicketAnalysis(BaseModel):
    category: str
    action: str
    reason: str