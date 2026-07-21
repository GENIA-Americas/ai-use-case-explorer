from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field

Complexity = Literal["low", "medium", "high"]


class UseCaseCreate(BaseModel):
    model_config = ConfigDict(extra="forbid")

    title: str = Field(min_length=1, max_length=200)
    industry: str = Field(min_length=1, max_length=100)
    category: str = Field(min_length=1, max_length=100)
    description: str = Field(min_length=1)
    complexity: Complexity
    tags: list[str] = Field(default_factory=list)


class UseCaseResult(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    industry: str
    category: str
    description: str
    complexity: str
    tags: list[str]
    created_at: datetime
