"""
Modèle pour l'output structuré du LLM
"""
from pydantic import BaseModel
from typing import Optional


class CriteresSchema(BaseModel):
    plage: Optional[bool] = None
    montagne: Optional[bool] = None
    ville: Optional[bool] = None
    sport: Optional[bool] = None
    detente: Optional[bool] = None
    acces_handicap: Optional[bool] = None
