from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un experto en analisis de sentimientos. Califica cada texto del usuario como positivo, negativo o neutral."),
    MessagesPlaceholder(variable_name="ejemplo"),
    ("human", "{mensaje}")
])

ejemplo_sentimientos = [
    HumanMessage(content="Me encanta este producto, es fantástico!"),
    AIMessage(content="Sentimiento: Positivo"),
    HumanMessage(content="No me gusta este servicio, es terrible."),
    AIMessage(content="Sentimiento: Negativo"),
    HumanMessage(content="El producto es aceptable, pero podría mejorar."),
    AIMessage(content="Sentimiento: Neutral")
]

mensajes = chat_prompt.format_messages(
    ejemplo=ejemplo_sentimientos,
    mensaje="El servicio al cliente fue excelente, estoy muy satisfecho."
)

for i, m in enumerate(mensajes):
    print(f"Mensaje {i+1}: {m.__class__.__name__}")
    print(m.content)
    print("---")