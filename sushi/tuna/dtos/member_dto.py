from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from enum import Enum


class MemberDTO:
    member_id: int
    email: str
    first_name: str
    last_name: str
    member_type: str
    organization_id: int
    organization_name: str


    def __init__(self, email, first_name, last_name, member_type):
        self.email=email
        self.first_name=first_name
        self.last_name=last_name
        self.member_type=member_type

    def to_json(self):
        return  {
            "member_id": self.member_id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "member_type": self.member_type,
            "organization_id": self.organization_id,
            "organization_name": self.organization_name
        }

    @staticmethod
    def from_google_user(google_user):
        return MemberDTO(
            email=google_user.get('email'),
            first_name=google_user.get('given_name'),
            last_name=google_user.get('family_name'),
            member_type = 'admin'
        )

    

class Organization(BaseModel):
    organzation_id: int
    name: str
    industry: str
    website: str
    city: str
    country: str



