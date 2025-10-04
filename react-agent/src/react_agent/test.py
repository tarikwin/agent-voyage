# # Graphe LangGraph pour l'agent de voyage

# from __future__ import annotations
# from dataclasses import dataclass, field
# from typing import Any

# from langchain.chat_models import init_chat_model
# from langgraph.graph import START, END, StateGraph

# from src.react_agent.trips import VOYAGES_POSSIBLES
# from src.react_agent.prompts import construire_prompt_reponse

# # Modèle LLM
# MODEL_NAME = "mistral-small-latest"

# # Critères utilisateur
# @dataclass
# class Criteres:
#     criteres: dict[str, bool | None] = field(default_factory=lambda: {
#         "plage": None,
#         "montagne": None,
#         "ville": None,
#         "sport": None,
#         "detente": None,
#         "acces_handicap": None,
#     })

#     def detecter_depuis_texte(self, texte: str) -> None:
#         texte = texte.lower()
#         for critere in self.criteres.keys():
#             if critere in texte:
#                 self.criteres[critere] = True
#             elif critere not in texte:
#                 self.criteres[critere] = False

#     def au_moins_un_rempli(self) -> bool:
#         return any(v is True for v in self.criteres.values())

# # État du graphe
# @dataclass
# class State:
#     message_utilisateur: str = ""
#     message_ia: str = ""
#     done: bool = False
#     criteres: Criteres = field(default_factory=Criteres)

# # Étape 1 : mise à jour des critères
# async def mise_a_jour_criteres(state: State) -> dict[str, Any]:
#     state.criteres.detecter_depuis_texte(state.message_utilisateur)
#     return {"criteres": state.criteres}

# # Étape 2 : choix du voyage et génération de réponse
# async def choix_voyage_et_question(state: State) -> dict[str, Any]:
#     model = init_chat_model(model=MODEL_NAME, model_provider="mistralai")
#     prompt = construire_prompt_reponse(
#         message_utilisateur=state.message_utilisateur,
#         criteres=state.criteres.criteres,
#         voyages_possibles=VOYAGES_POSSIBLES,
#         au_moins_un_critere_rempli=state.criteres.au_moins_un_rempli()
#     )
#     res = await model.ainvoke(prompt)
#     return {"message_ia": res.content}

# # Création du graphe LangGraph
# graph = (
#     StateGraph(State)
#     .add_node(mise_a_jour_criteres)
#     .add_node(choix_voyage_et_question)
#     .add_edge(START, mise_a_jour_criteres.__name__)
#     .add_edge(mise_a_jour_criteres.__name__, choix_voyage_et_question.__name__)
#     .add_edge(choix_voyage_et_question.__name__, END)
#     .compile(name="Agent de voyage (2 étapes)")
# )
