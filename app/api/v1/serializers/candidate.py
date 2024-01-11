import uuid
from enum import Enum
from typing import List

from pydantic import BaseModel, EmailStr, validator

from app.api.v1.serializers.response import BaseResponse
from core.exceptions.profile import InvalidYearExperience, InvalidCareerLevel, InvalidGender, InvalidSalary


class CareerLevel(Enum):
    JUNIOR = "Junior"
    SENIOR = "Senior"
    MID_LEVEL = "Mid Level"


class DegreeType(Enum):
    BACHELOR = "Bachelor"
    MASTER = "Master"
    HIGH_SCHOOL = "High School"


class Gender(Enum):
    MALE = "Male"
    FEMALE = "Female"
    NOT_SPECIFIED = "Not Specified"


class Candidate(BaseModel):
    first_name: str
    last_name: str
    email: EmailStr
    uuid: str = uuid.uuid4()
    career_level: CareerLevel
    job_major: str
    years_of_experience: int
    degree_type: DegreeType
    skills: List[str]
    nationality: str
    city: str
    salary: float
    gender: Gender

    @validator('years_of_experience')
    def validate_experience(cls, v):
        if v < 0:
            raise InvalidYearExperience
        return v

    @validator('career_level')
    def validate_career_level(cls, v):
        if v not in CareerLevel:
            raise InvalidCareerLevel
        return v

    @validator('gender')
    def validate_gender(cls, v):
        if v not in Gender:
            raise InvalidGender
        return v

    @validator('salary')
    def validate_salary(cls, v):
        if type(v) is not float:
            raise InvalidSalary
        return v


class CandidateResponse(BaseResponse):
    data: List[Candidate]
