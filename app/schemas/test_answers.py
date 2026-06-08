from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Annotated, Optional, Union, Literal
from datetime import datetime

from ..models.context.enums import QuestionTypes, ReviewModes, ScoringType
from ..utils.schemas_utils import optional

class Answer(BaseModel):
    title: Annotated[str, Field()]
    type: Annotated[QuestionTypes, Field(...)]


class WriteAnswer(Answer):
    type: Literal[QuestionTypes.WRITE_ANSWER] = QuestionTypes.WRITE_ANSWER
    answer: Annotated[str, Field(..., max_length=1000)]


class SelectOneAnswer(Answer):
    type: Literal[QuestionTypes.SELECT_ONE] = QuestionTypes.SELECT_ONE
    options: Annotated[list[str], Field(min_length=1)]
    answer: Annotated[str, Field(...,min_length=1, max_length=1000)]

class SelectMultipleAnswer(Answer):
    type: Literal[QuestionTypes.SELECT_MULTIPLE] = QuestionTypes.SELECT_MULTIPLE
    options: Annotated[list[str], Field(min_length=1)]
    answer: Annotated[list[str], Field(..., min_length=1)]


class MatchAnswer(Answer):
    type: Literal[QuestionTypes.MATCH] = QuestionTypes.MATCH
    left_column: Annotated[list[str], Field()]
    right_column: Annotated[list[str], Field()]
    answer: Annotated[dict[str, str], Field(..., min_length=1)]


Answers = Annotated[
    Union[SelectOneAnswer, SelectMultipleAnswer, WriteAnswer, MatchAnswer],
    Field(discriminator='type')
]

class AnswerBase(BaseModel):
    test_id: Annotated[int, Field(..., ge=1)]
    user_id: Annotated[int, Field(..., ge=1)]
    start_time: Annotated[datetime, Field(...)]
    end_time: Annotated[datetime, Field(...)]
    answers: Annotated[list[Answers], Field(...)]
    
class AnswerCreate(AnswerBase):
    ...


@optional
class AnswerUpdate(AnswerCreate):
    ...
    

class AnswerResponse(AnswerBase):
    model_config = ConfigDict(from_attributes=True)