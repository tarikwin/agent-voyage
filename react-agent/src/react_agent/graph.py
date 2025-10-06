from __future__ import annotations
from typing import Any
from langchain.chat_models import init_chat_model
from langgraph.graph import START, END, StateGraph
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser

from react_agent.data.trips import VOYAGES_POSSIBLES
from react_agent.prompts import construire_prompt_reponse
from react_agent.models.state import State
from react_agent.models.criteres import Criteres
from react_agent.models.criteres_schema import CriteresSchema

MODEL_NAME = "mistral-small-latest"

async def traiter_message(state: State) -> dict[str, Any]:
    model = init_chat_model(model=MODEL_NAME, model_provider="mistralai")

    prompt = ChatPromptTemplate.from_template("""
Tu es un assistant qui aide à planifier un voyage.

Analyse ce message utilisateur : "{message_utilisateur}".

Retourne un JSON :
{{
  "plage": true/false/null,
  "montagne": true/false/null,
  "ville": true/false/null,
  "sport": true/false/null,
  "detente": true/false/null,
  "acces_handicap": true/false/null
}}
""")

    parser = JsonOutputParser(pydantic_object=CriteresSchema)
    chain = prompt | model | parser

    criteres_structures = await chain.ainvoke(
        {"message_utilisateur": state.message_utilisateur}
    )

    # Mise à jour du state (criteres_structures est déjà un dict)
    state.criteres.criteres.update(criteres_structures)

    if not state.criteres.au_moins_un_requis():
        state.message_ia = (
            "Je n’ai pas compris tes préférences. "
            "Peux-tu me préciser ce que tu recherches : plage, montagne, ville, sport, détente, accessibilité ?"
        )
        return {"message_ia": state.message_ia}

    prompt_reco = construire_prompt_reponse(
        message_utilisateur=state.message_utilisateur,
        criteres=state.criteres.criteres,
        voyages_possibles=VOYAGES_POSSIBLES,
        au_moins_un_critere_rempli=True
    )

    res = await model.ainvoke(prompt_reco)
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
