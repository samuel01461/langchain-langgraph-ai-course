from langchain_core.runnables import RunnableLambda

paso1 = RunnableLambda(lambda x: f"Numero {x}")

def duplicar(texto):
    return [texto] * 2

paso2 = RunnableLambda(duplicar)

cadena = paso1 | paso2

resultado = cadena.invoke("1")

print(resultado)