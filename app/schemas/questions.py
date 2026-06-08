from pydantic import BaseModel, Field, ConfigDict, model_validator
from typing import Annotated, Optional, Union, Literal
from datetime import datetime

from ..models.context.enums import QuestionTypes, ReviewModes, ScoringType


class Scoring(BaseModel):
    method: Annotated[ScoringType, Field(default=ScoringType.EXACT)]
    points: Annotated[Optional[int], Field(default=None)]
    min_points: Annotated[Optional[int], Field(default=None)]
    max_points: Annotated[Optional[int], Field(default=None)]
    points_per_right: Annotated[Optional[int], Field(default=None)]
    penalty_per_wrong: Annotated[Optional[int], Field(default=None)]
    


class QuestionBase(BaseModel):
    type: Annotated[QuestionTypes, Field(...)]
    text: Annotated[str, Field(max_length=1000)]
    review_mode: Annotated[ReviewModes, Field(default=ReviewModes.AUTO)]
    scoring: Scoring


class SelectOneQuestion(QuestionBase):
    type: Literal[QuestionTypes.SELECT_ONE] = QuestionTypes.SELECT_ONE
    options: Annotated[list[str], Field(min_length=1)]
    answers: Annotated[list[str], Field(min_length=1, max_length=1)]
    
    
    # @model_validator(mode='after')
    # def check_answers_in_options(self):
    #     for ans in self.answers:
    #         if ans not in self.options:
    #             raise ValueError(f"Answer '{ans}' not found in options")
    #     return self




class SelectMultipleQuestion(SelectOneQuestion):
    type: Literal[QuestionTypes.SELECT_MULTIPLE] = QuestionTypes.SELECT_MULTIPLE
    answers: Annotated[list[str], Field(min_length=1)]
    

class WriteAnswer(QuestionBase):
    type: Literal[QuestionTypes.WRITE_ANSWER] = QuestionTypes.WRITE_ANSWER
    answer: Annotated[str, Field(max_length=1000)]


class MatchQuestion(QuestionBase):
    type: Literal[QuestionTypes.MATCH] = QuestionTypes.MATCH
    left_column: Annotated[list[str], Field()]
    right_column: Annotated[list[str], Field()]
    answers: Annotated[dict[str, str], Field()]
    
    # @model_validator(mode="after")
    # def validate_match(self):
    #     for left, right in self.answers.items():
    #         if left not in self.left_column:
    #             raise ValueError(f"Left key '{left}' not in left_column")
    #         if right not in self.right_column:
    #             raise ValueError(f"Right value '{right}' not in right_column")
    #     return self
    

Question = Annotated[
    Union[SelectOneQuestion, SelectMultipleQuestion, WriteAnswer, MatchQuestion],
    Field(discriminator='type')
]