from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from datetime import datetime
from typing import Optional

from ..models.course import Test, UserAttemps
from ..schemas.tests import TestCreate, TestUpdate
from ..schemas.test_answers import AnswerCreate

class TestService:
    def __init__(self, session: Session) -> None:
        self._db = session
    
    
    def list_tests(self, skip: int = 0, limit: int = 100) -> list[Test]:
        stmt = select(Test).offset(skip).limit(limit)
        return list(self._db.scalars(stmt).all())


    def get_test(self, test_id: int) -> Optional[Test]:
        return self._db.get(Test, test_id)
    
    
    def create_test(self, test_schema: TestCreate) -> Test:
        test = Test(**test_schema.model_dump())
        
        self._db.add(test)
        self._db.commit()
        self._db.refresh(test)
        
        return test


    def update_test(self, test_id: int, test_schema: TestUpdate) -> Test:
        test = self._get_test_or_raise(test_id)
        
        update_dict = test_schema.model_dump(exclude_unset=True)
        
        for field, value in update_dict.items():
            setattr(test, field, value)

        test.last_change_date = datetime.now()
        
        self._db.commit()
        self._db.refresh(test)
        
        return test
        
    
    def delete_test(self, test_id: int):
        test = self._get_test_or_raise(test_id)
        
        self._db.delete(test)
        self._db.commit()
        
    
    def get_attempts(self, test_id: int, user_id: Optional[int] = None) -> list[UserAttemps]:
        stmt = select(UserAttemps).filter(UserAttemps.test_id == test_id)
        
        if user_id is not None:
            stmt.filter(UserAttemps.user_id == user_id)
        
        return list(self._db.scalars(stmt).all())
    
    
    
    def create_attempt(self, test_id: int, attempt_data: AnswerCreate):
        test = self._get_test_or_raise(test_id)
        
        if test.content is None:
            raise ValueError()
        
        
        total_score, max_score = self._compute_score(test.content, attempt_data.answers)
        
        print(attempt_data.model_dump())
        
        attempt = UserAttemps(**attempt_data.model_dump())
        attempt.test_id = test_id
        attempt.score = round(total_score)
        attempt.max_score = max_score

        self._db.add(attempt)
        self._db.commit()
        self._db.refresh(attempt)
        

    
    def _get_test_or_raise(self, test_id: int) -> Test:
        test = self.get_test(test_id)
        if not test:
            raise NoResultFound
        return test
    
    def _compute_score(self, test_content: list[str], user_answers: list) -> list[int]:
        total_score = 0
        max_score = 0

        for question, user_answer in zip(test_content, user_answers):
            q_type = question["type"]
            scoring = question["scoring"]
            method = scoring.get("method", "exact")
            

            if q_type == "select_one":
                correct = question["answers"][0]
                user = user_answer.answer
                is_correct = (user == correct)

                question_points = scoring.get("points", 0)
                points = question_points if is_correct else 0
                max_score += question_points

            elif q_type == "select_multiple":
                correct_set = set(question["answers"])
                user_set = set(user_answer.answer)

                if method == "exact":
                    is_correct = (correct_set == user_set)
                    question_points = scoring.get("points", 0)
                    points = question_points if is_correct else 0
                    max_score += question_points
                else:
                    correct_selected = len(correct_set & user_set)
                    incorrect_selected = len(user_set - correct_set)
                    points = (correct_selected * scoring.get("points_per_right", 0)) - \
                            (incorrect_selected * scoring.get("penalty_per_wrong", 0))
                    min_pts = scoring.get("min_points", 0)
                    max_pts = scoring.get("max_points", scoring.get("points", 0))
                    max_score += max_pts
                    points = max(min_pts, min(max_pts, points))

            elif q_type == "write_answer":
                correct = question["answer"]
                user = user_answer.answer
                is_correct = (user.strip() == correct.strip())
                question_points = scoring.get("points", 0)
                points = question_points if is_correct else 0
                max_score += scoring.get("points", 0)

            elif q_type == "match_answers":
                correct_pairs = question["answers"]
                user_pairs = user_answer.answer
                
                if method == "exact":
                    is_correct = (correct_pairs == user_pairs)
                    question_points = scoring.get("points", 0) 
                    points = question_points if is_correct else 0
                    max_score += scoring.get("points", 0) 
                else:  # partial: each correct match gives points_per_right
                    correct_matches = 0
                    for left, right in user_pairs.items():
                        if correct_pairs.get(left) == right:
                            correct_matches += 1
                    points = correct_matches * scoring.get("points_per_right", 0)
                    wrong_matches = len(user_pairs) - correct_matches
                    points -= wrong_matches * scoring.get("penalty_per_wrong", 0)
                    min_pts = scoring.get("min_points", 0)
                    max_pts = scoring.get("max_points", scoring.get("points", 0))
                    max_score += max_pts
                    points = max(min_pts, min(max_pts, points))

            else:
                points = 0

            total_score += points

        return [total_score, max_score]