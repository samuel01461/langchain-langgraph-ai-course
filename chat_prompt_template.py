from langchain_core.prompts import ChatPromptTemplate

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un traductor de español a inglés."),
    ("human", "{texto}")
])

mensajes = chat_prompt.format_messages(texto="Hola, ¿cómo estás?")

for m in mensajes:
    print(f"{type(m)}: {m.content}")