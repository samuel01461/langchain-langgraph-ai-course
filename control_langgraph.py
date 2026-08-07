from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    numero: int
    resultado: str

graph = StateGraph(State)
def caso_par(state):
    return {"resultado": "El número es par"}

def caso_impar(state):
    return {"resultado": "El número es impar"}

graph.add_node("CasoPar", caso_par)
graph.add_node("CasoImpar", caso_impar)

def decidir_rama(state):
    if state["numero"] % 2 == 0:
        return "CasoPar"
    else:
        return "CasoImpar"

graph.add_conditional_edges(START, decidir_rama)
graph.add_edge("CasoPar", END)
graph.add_edge("CasoImpar", END)

compiled = graph.compile()
print(compiled.invoke({"numero": 5}))