from fastapi import FastAPI
from pydantic import BaseModel
from react_agent.graph import graph, State  # ton graphe et la dataclass State

app = FastAPI(title="Agent de Voyage")


class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
async def chat(request: ChatRequest):
    # Crée l'état initial à partir du message utilisateur
    state = State(message_utilisateur=request.message)
    
    # Exécute le graphe compilé avec invoke()
    result_state = await graph.ainvoke(state)
    
    return {
        "criteres": result_state["criteres"].criteres,
        "message_ia": result_state["message_ia"]
    }
