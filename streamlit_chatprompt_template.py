import streamlit as st
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain.prompts import ChatPromptTemplate

st.set_page_config(page_title="Chatbot basico", page_icon=":robot_face:")
st.title("Chatbot basico con langchain ")
st.markdown("Este es un ejemplo de un chatbot básico utilizando LangChain y Streamlit.")

with st.sidebar:
    st.header("Configuración del modelo")
    model_name = st.selectbox("Selecciona el modelo de OpenAI", ["gpt-3.5-turbo", "gpt-4", "gpt-4o-mini"])
    temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)

    personalidades = st.selectbox("Selecciona la personalidad del asistente", [
        "Asistente amigable",
        "Asistente formal"
    ])
    chat_model = ChatOpenAI(model_name=model_name, temperature=temperature)

    system_messages = {
        "Asistente amigable": "Eres un asistente útil y amigable.",
        "Asistente formal": "Eres un asistente profesional y formal."
    }

    chat_prompt = ChatPromptTemplate.from_messages([
        ("system", system_messages[personalidades]),
        ("human", "{mensaje}")
    ])

    cadena = chat_prompt | chat_model

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

for msg in st.session_state.mensajes:
    if isinstance(msg, HumanMessage):
        continue
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

if st.button("Limpiar conversación"):
    st.session_state.mensajes = []
    st.experimental_rerun()

pregunta = st.chat_input("Escribe tu mensaje:")

if pregunta:
    with st.chat_message("user"):
        st.markdown(pregunta)

    historial_text = ""

    for msg in st.session_state.mensajes[-10:]:
        if isinstance(msg, HumanMessage):
            historial_text += f"Usuario: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            historial_text += f"Asistente: {msg.content}\n"

    if not historial_text:
        historial_text = "No hay historial de conversación."

    try:
        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            full_response = ""

            for chunk in cadena.stream({"mensaje": pregunta, "historial": historial_text}):
                full_response += chunk.content
                response_placeholder.markdown(full_response + "▌")

            st.session_state.mensajes.append(HumanMessage(content=pregunta))
            st.session_state.mensajes.append(AIMessage(content=full_response))
    except Exception as e:
        st.error(f"Error al generar la respuesta: {e}")