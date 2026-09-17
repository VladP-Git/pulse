from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict, StringConstraints, TypeAdapter


QuestionText = Annotated[str, StringConstraints(strip_whitespace=True, min_length=5, max_length=100)]


class QuestionBase(BaseModel):
    text: QuestionText


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(QuestionBase):
    text: QuestionText | None = None


class QuestionRead(QuestionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


QuestionsList = TypeAdapter(list[QuestionRead])
