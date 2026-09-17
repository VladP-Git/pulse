from typing import Annotated
from pydantic import BaseModel, Field, ConfigDict, TypeAdapter

QuestionText = Annotated[
    str, Field(min_length=1, max_length=256, strip_whitespace=True, description="Text of the question")
]
QuestionId = Annotated[int, Field(description="ID of the question")]


class QuestionBase(BaseModel):
    text: QuestionText


class QuestionCreate(QuestionBase):
    pass


class QuestionRead(QuestionBase):
    model_config = ConfigDict(from_attributes=True)
    id: QuestionId


class QuestionUpdate(QuestionBase):
    pass

QuestionsList = TypeAdapter(list[QuestionRead])