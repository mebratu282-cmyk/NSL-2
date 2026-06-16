from pydantic import BaseModel


class ApprovalRequest(BaseModel):
    approval_comment: str | None = None