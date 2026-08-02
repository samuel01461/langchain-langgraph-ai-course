from langchain_core.runnables import RunnableLambda
from langchain_openai import ChatOpenAI
import json

llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)

def preprocesar_texto(texto):
    return texto.strip()[:500]

preprocesar = RunnableLambda(preprocesar_texto) 

def generar_resumen(texto):
    prompt = f"Por favor resume en una sola linea:\n\n{texto}"
    respuesta = llm.invoke(prompt)
    return respuesta.content

def analizar_sentimiento(texto):
    prompt = f"""Analiza el sentimiento del siguiente texto y responde unicamente en formato JSON valido: 
    {{"sentimiento": "positivo|negativo|neutro", "razon": "breve explicacion"}}
    \n\n{texto}"""  
    respuesta = llm.invoke(prompt)
    
    try:
        sentimiento_json = json.loads(respuesta.content)
        return sentimiento_json
    except json.JSONDecodeError:
        return {"sentimiento": "neutro", "razon": "No se pudo parsear la respuesta a JSON"}

def merge_results(data):
    return {
        "resumen": data["resumen"],
        "sentimiento": data["sentimiento_data"]["sentimiento"],
        "razon": data["sentimiento_data"]["razon"]
    }

def process_one(texto):
    resumen = generar_resumen(texto)
    sentimiento_data = analizar_sentimiento(texto)
    
    return merge_results(resumen, sentimiento_data)

process = RunnableLambda(process_one)
chain = preprocesar | process