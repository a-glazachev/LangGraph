"""
Module: graph/editor_decision.py
Description:
    This module is responsible for editor decision
"""

from pydantic import BaseModel, Field


class EditorDecision(BaseModel):
    approved: bool = Field(description="Approve flag from the editor: yes/no")
    details: str = Field(description="Detailed response from the editor")
