from dataclasses import dataclass
from typing import List

@dataclass
class Group:
    group_id: int
    group_name: str
    invite_code: str

@dataclass
class Member:
    member_id: int
    group_id: int
    name: str
    budget: int
    allergies: List[str]
    likes: List[str]
    dislikes: List[str]