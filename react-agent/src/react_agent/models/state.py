#  Définition de l’état du graphe

from dataclasses import dataclass, field
from react_agent.models.criteres import Criteres

@dataclass
class State:
    message_utilisateur: str = ""
    message_ia: str = ""
    done: bool = False
    criteres: Criteres = field(default_factory=Criteres)
