# centralisation des prompts

from typing import Dict, List

def construire_prompt_reponse(
    message_utilisateur: str,
    criteres: Dict[str, bool | None],
    voyages_possibles: List[Dict],
    au_moins_un_critere_rempli: bool
) -> str:
    """
    Construit le prompt à envoyer au LLM selon l'état actuel de l'utilisateur.
    """
    prompt = f"""
Tu es un agent de voyage professionnel, aimable et attentionné.
Ton objectif est de comprendre les attentes du client et de lui proposer un voyage idéal.

Message utilisateur :
{message_utilisateur}

Critères détectés :
{criteres}

Voyages disponibles :
{voyages_possibles}
"""

    if not au_moins_un_critere_rempli:
        prompt += """
L'utilisateur n'a pas encore précisé ses critères de voyage.
Pose-lui une question ouverte et naturelle pour comprendre ses préférences :
destination (plage, montagne, ville), activités (sport, détente...), ambiance, accessibilité...
"""
    else:
        prompt += """
Propose-lui le voyage le plus adapté aux critères détectés.
Explique ton choix en quelques phrases, de façon claire et engageante.
"""

    return prompt.strip()
