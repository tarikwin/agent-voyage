# Définition de la classe Criteres

from dataclasses import dataclass, field

@dataclass
class Criteres:
    criteres: dict[str, bool | None] = field(default_factory=lambda: {
        "plage": None,
        "montagne": None,
        "ville": None,
        "sport": None,
        "detente": None,
        "acces_handicap": None,
    })

    def au_moins_un_requis(self) -> bool:
        """Retourne True si au moins un critère est True"""
        return any(v is True for v in self.criteres.values())
