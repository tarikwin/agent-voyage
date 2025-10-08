from __future__ import annotations
from typing import Any

from langchain.chat_models import init_chat_model
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from langgraph.graph import START, END, StateGraph

from react_agent.models.state import State
from react_agent.models.criteres_schema import CriteresSchema
from react_agent.prompts import construire_prompt_reponse
from react_agent.data.trips import VOYAGES_POSSIBLES

MODEL_NAME = "mistral-small-latest"


async def traiter_message(state: State) -> dict[str, Any]:
    """
    Étape principale du graphe : analyse le message utilisateur,
    extrait les critères de voyage, et propose une recommandation.
    """
    # Initialisation du modèle
    model = init_chat_model(model=MODEL_NAME, model_provider="mistralai")

    # Construction du prompt pour l’analyse du message
    prompt_criteres = ChatPromptTemplate.from_template("""
Tu es un assistant qui aide à planifier un voyage.

Analyse ce message utilisateur : "{message_utilisateur}".

Retourne un JSON conforme au schéma suivant :
{{
  "plage": true/false/null,
  "montagne": true/false/null,
  "ville": true/false/null,
  "sport": true/false/null,
  "detente": true/false/null,
  "acces_handicap": true/false/null
}}
""")

    # Chaîne de traitement (prompt --> LLM --> parsing JSON)
    parser = JsonOutputParser(pydantic_object=CriteresSchema)
    chain_criteres = prompt_criteres | model | parser

    criteres_structures = await chain_criteres.ainvoke(
        {"message_utilisateur": state.message_utilisateur}
    )

    # Mise à jour du state
    state.criteres.criteres.update(criteres_structures)

    # Si aucun critère n’est détecté, demander clarification
    if not state.criteres.au_moins_un_requis():
        state.message_ia = (
            "Je n’ai pas compris tes préférences. "
            "Peux-tu préciser ce que tu recherches : plage, montagne, ville, sport, détente, accessibilité ?"
        )
        return {"message_ia": state.message_ia}

    # Construction du prompt de recommandation
    prompt_reco = construire_prompt_reponse(
        message_utilisateur=state.message_utilisateur,
        criteres=state.criteres.criteres,
        voyages_possibles=VOYAGES_POSSIBLES,
        au_moins_un_critere_rempli=True
    )

    # Appel au modèle pour la recommandation finale
    res = await model.ainvoke(prompt_reco)
    state.message_ia = res.content

    return {
        "criteres": state.criteres,
        "message_ia": state.message_ia
    }


# Définition du graphe LangGraph
graph = (
    StateGraph(State)
    .add_node(traiter_message)
    .add_edge(START, traiter_message.__name__)
    .add_edge(traiter_message.__name__, END)
    .compile(name="Agent de voyage")
)
