from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class UserModel:
    id: int
    created_at: datetime
    current_model: str
    api_key: Optional[str]
    long_memory: bool
    last_character_id: Optional[int]
    is_admin: bool

@dataclass
class CharacterModel:
    id: Optional[int]
    user_id: int
    name: str
    prompt: str
    created_at: Optional[datetime] = None