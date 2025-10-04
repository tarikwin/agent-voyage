# Définition de la classe Criteres

from dataclasses import dataclass, field
from react_agent.data.mots_cles import MOTS_CLES

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

    def intercepter_criteres(self, texte: str) -> bool:
        """Détecte les critères dans le texte et met à jour le dictionnaire"""
        texte = texte.lower()
        any_detected = False

        # Détection des critères par mots-clés
        for critere, mots in MOTS_CLES.items():
            if any(mot in texte for mot in mots):
                self.criteres[critere] = True
                any_detected = True

        # Si aucun critère détecté → reset complet
        if not any_detected:
            for critere in self.criteres.keys():
                self.criteres[critere] = None
        else:
            # Sinon, les critères non mentionnés passent à False
            for critere, valeur in self.criteres.items():
                if valeur is None:
                    self.criteres[critere] = False

        return any_detected

    def au_moins_un_requis(self) -> bool:
        """Retourne True si au moins un critère est True"""
        return any(v is True for v in self.criteres.values())
