from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class State(TypedDict):
    text_original: str
    texto_mayus: str
    longitud: int

graph = StateGraph(State)

def mayusculas(state):
    return {"texto_mayus": state["text_original"].upper()}

def contador(state):
    return {"longitud": len(state["text_original"])}

graph.add_node("Mayusculas", mayusculas)
graph.add_node("Contador", contador)

graph.add_edge(START, "Mayusculas")
graph.add_edge("Mayusculas", "Contador")
graph.add_edge("Contador", END)

compilled_graph = graph.compile()

res = compilled_graph.invoke({"text_original": "Hola mundo"})
print(res)