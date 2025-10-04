# Graphe LangGraph principal

from __future__ import annotations
from typing import Any
from langchain.chat_models import init_chat_model
from langgraph.graph import START, END, StateGraph

from react_agent.data.trips import VOYAGES_POSSIBLES
from react_agent.prompts import construire_prompt_reponse
from react_agent.models.state import State

MODEL_NAME = "mistral-small-latest"

async def traiter_message(state: State) -> dict[str, Any]:
    any_detected = state.criteres.intercepter_criteres(state.message_utilisateur)

    if not any_detected:
        state.message_ia = (
            "Je n’ai pas compris tes préférences. "
            "Peux-tu me préciser ce que tu recherches : plage, montagne, ville, sport, détente, accessibilité ?"
        )
        return {"criteres": state.criteres, "message_ia": state.message_ia}

    model = init_chat_model(model=MODEL_NAME, model_provider="mistralai")
    prompt = construire_prompt_reponse(
        message_utilisateur=state.message_utilisateur,
        criteres=state.criteres.criteres,
        voyages_possibles=VOYAGES_POSSIBLES,
        au_moins_un_critere_rempli=state.criteres.au_moins_un_requis()
    )
    res = await model.ainvoke(prompt)
    state.message_ia = res.content

    return {"criteres": state.criteres, "message_ia": state.message_ia}

# Création du graphe LangGraph
graph = (
    StateGraph(State)
    .add_node(traiter_message)
    .add_edge(START, traiter_message.__name__)
    .add_edge(traiter_message.__name__, END)
    .compile(name="Agent de voyage (node unique)")
)
