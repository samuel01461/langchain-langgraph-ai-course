from langchain_core.runnables import RunnableLambda, RunnableParallel
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

resumen_branch = RunnableLambda(generar_resumen)

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

sentimiento_branch = RunnableLambda(analizar_sentimiento)

def merge_results(data):
    return {
        "resumen": data["resumen"],
        "sentimiento": data["sentimiento_data"]["sentimiento"],
        "razon": data["sentimiento_data"]["razon"]
    }

merge_branch = RunnableLambda(merge_results)

parallel_analysis = RunnableParallel({
    "resumen": resumen_branch,
    "sentimiento_data": sentimiento_branch
})

chain = preprocesar | parallel_analysis | merge_branch

review_batch = [
    "Me encantó el producto, superó mis expectativas.",
    "El servicio fue terrible, no lo recomiendo.",
    "Es un producto promedio, nada especial."
]

resultado_batch = chain.batch(review_batch)

print(resultado_batch)